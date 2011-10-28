// Copyright (c) 2011 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

/**
 * @fileoverview
 * Functions related to the 'host screen' for Chromoting.
 */

'use strict';

/** @suppress {duplicate} */
var remoting = remoting || {};

(function() {

/**
 * @type {boolean} Whether or not the last share was cancelled by the user.
 *     This controls what screen is shown when the host plugin signals
 *     completion.
 */
var lastShareWasCancelled_ = false;

/**
 * Start a host session. This is the main entry point for the host screen,
 * called directly from the onclick action of a button on the home screen.
 */
remoting.tryShare = function() {
  remoting.debug.log('Attempting to share...');
  lastShareWasCancelled_ = false;
  if (remoting.oauth2.needsNewAccessToken()) {
    remoting.debug.log('Refreshing token...');
    remoting.oauth2.refreshAccessToken(function() {
      if (remoting.oauth2.needsNewAccessToken()) {
        // If we still need it, we're going to infinite loop.
        showShareError_(/*i18n-content*/'ERROR_AUTHENTICATION_FAILED');
        throw 'Unable to get access token';
      }
      remoting.tryShare();
    });
    return;
  }

  onNatTraversalPolicyChanged_(true);  // Hide warning by default.
  remoting.setMode(remoting.AppMode.HOST_WAITING_FOR_CODE);
  document.getElementById('cancel-button').disabled = false;
  disableTimeoutCountdown_();

  var div = document.getElementById('host-plugin-container');
  remoting.hostSession = new remoting.HostSession();
  remoting.hostSession.createPluginAndConnect(
      document.getElementById('host-plugin-container'),
      /** @type {string} */(remoting.oauth2.getCachedEmail()),
      remoting.oauth2.getAccessToken(),
      onNatTraversalPolicyChanged_,
      onHostStateChanged_,
      logDebugInfo_);
};

/**
 * Callback for the host plugin to notify the web app of state changes.
 * @param {remoting.HostSession.State} state The new state of the plugin.
 */
function onHostStateChanged_(state) {
  if (state == remoting.HostSession.State.STARTING) {
    // Nothing to do here.
    remoting.debug.log('Host plugin state: STARTING');

  } else if (state == remoting.HostSession.State.REQUESTED_ACCESS_CODE) {
    // Nothing to do here.
    remoting.debug.log('Host plugin state: REQUESTED_ACCESS_CODE');

  } else if (state == remoting.HostSession.State.RECEIVED_ACCESS_CODE) {
    remoting.debug.log('Host plugin state: RECEIVED_ACCESS_CODE');
    var accessCode = remoting.hostSession.getAccessCode();
    var accessCodeDisplay = document.getElementById('access-code-display');
    accessCodeDisplay.innerText = '';
    // Display the access code in groups of four digits for readability.
    var kDigitsPerGroup = 4;
    for (var i = 0; i < accessCode.length; i += kDigitsPerGroup) {
      var nextFourDigits = document.createElement('span');
      nextFourDigits.className = 'access-code-digit-group';
      nextFourDigits.innerText = accessCode.substring(i, i + kDigitsPerGroup);
      accessCodeDisplay.appendChild(nextFourDigits);
    }
    accessCodeExpiresIn_ = remoting.hostSession.getAccessCodeLifetime();
    if (accessCodeExpiresIn_ > 0) {  // Check it hasn't expired.
      accessCodeTimerId_ = setInterval(
          'remoting.decrementAccessCodeTimeout_()', 1000);
      timerRunning_ = true;
      updateAccessCodeTimeoutElement_();
      updateTimeoutStyles_();
      remoting.setMode(remoting.AppMode.HOST_WAITING_FOR_CONNECTION);
    } else {
      // This can only happen if the cloud tells us that the code lifetime is
      // <= 0s, which shouldn't happen so we don't care how clean this UX is.
      remoting.debug.log('Access code already invalid on receipt!');
      remoting.cancelShare();
    }

  } else if (state == remoting.HostSession.State.CONNECTED) {
    remoting.debug.log('Host plugin state: CONNECTED');
    var element = document.getElementById('host-shared-message');
    var client = remoting.hostSession.getClient();
    l10n.localizeElement(element, client);
    remoting.setMode(remoting.AppMode.HOST_SHARED);
    disableTimeoutCountdown_();

  } else if (state == remoting.HostSession.State.DISCONNECTING) {
    remoting.debug.log('Host plugin state: DISCONNECTING');

  } else if (state == remoting.HostSession.State.DISCONNECTED) {
    remoting.debug.log('Host plugin state: DISCONNECTED');
    if (remoting.currentMode != remoting.AppMode.HOST_SHARE_FAILED) {
      // If an error is being displayed, then the plugin should not be able to
      // hide it by setting the state. Errors must be dismissed by the user
      // clicking OK, which puts the app into mode HOME.
      if (lastShareWasCancelled_) {
        remoting.setMode(remoting.AppMode.HOME);
      } else {
        remoting.setMode(remoting.AppMode.HOST_SHARE_FINISHED);
      }
    }
    remoting.hostSession.removePlugin();

  } else if (state == remoting.HostSession.State.ERROR) {
    remoting.debug.log('Host plugin state: ERROR');
    showShareError_(/*i18n-content*/'ERROR_GENERIC');
  } else {
    remoting.debug.log('Unknown state -> ' + state);
  }
}

/**
 * This is the callback that the host plugin invokes to indicate that there
 * is additional debug log info to display.
 * @param {string} msg The message (which will not be localized) to be logged.
 */
function logDebugInfo_(msg) {
  remoting.debug.log('plugin: ' + msg);
}

/**
 * Show a host-side error message.
 *
 * @param {string} errorTag The error message to be localized and displayed.
 * @return {void} Nothing.
 */
function showShareError_(errorTag) {
  var errorDiv = document.getElementById('host-plugin-error');
  l10n.localizeElementFromTag(errorDiv, errorTag);
  remoting.debug.log('Sharing error: ' + errorTag);
  remoting.setMode(remoting.AppMode.HOST_SHARE_FAILED);
}

/**
 * Cancel an active or pending share operation.
 *
 * @return {void} Nothing.
 */
remoting.cancelShare = function() {
  remoting.debug.log('Canceling share...');
  remoting.lastShareWasCancelled = true;
  try {
    remoting.hostSession.disconnect();
  } catch (error) {
    // Hack to force JSCompiler type-safety.
    var errorTyped = /** @type {{description: string}} */ error;
    remoting.debug.log('Error disconnecting: ' + errorTyped.description +
                       '. The host plugin probably crashed.');
    // TODO(jamiewalch): Clean this up. We should have a class representing
    // the host plugin, like we do for the client, which should handle crash
    // reporting and it should use a more detailed error message than the
    // default 'generic' one. See crbug.com/94624
    showShareError_(/*i18n-content*/'ERROR_GENERIC');
  }
  disableTimeoutCountdown_();
};

/**
 * @type {boolean} Whether or not the access code timeout countdown is running.
 */
var timerRunning_ = false;

/**
 * @type {number} The id of the access code expiry countdown timer.
 */
var accessCodeTimerId_ = 0;

/**
 * @type {number} The number of seconds until the access code expires.
 */
var accessCodeExpiresIn_ = 0;

/**
 * The timer callback function, which needs to be visible from the global
 * namespace.
 */
remoting.decrementAccessCodeTimeout_ = function() {
  --accessCodeExpiresIn_;
  updateAccessCodeTimeoutElement_();
};

/**
 * Stop the access code timeout countdown if it is running.
 */
function disableTimeoutCountdown_() {
  if (timerRunning_) {
    clearInterval(accessCodeTimerId_);
    timerRunning_ = false;
    updateTimeoutStyles_();
  }
}

/**
 * Constants controlling the access code timer countdown display.
 */
var ACCESS_CODE_TIMER_DISPLAY_THRESHOLD_ = 30;
var ACCESS_CODE_RED_THRESHOLD_ = 10;

/**
 * Show/hide or restyle various elements, depending on the remaining countdown
 * and timer state.
 *
 * @return {boolean} True if the timeout is in progress, false if it has
 * expired.
 */
function updateTimeoutStyles_() {
  if (timerRunning_) {
    if (accessCodeExpiresIn_ <= 0) {
      remoting.cancelShare();
      return false;
    }
    if (accessCodeExpiresIn_ <= ACCESS_CODE_RED_THRESHOLD_) {
      addClass(document.getElementById('access-code-display'), 'expiring');
    } else {
      removeClass(document.getElementById('access-code-display'), 'expiring');
    }
  }
  document.getElementById('access-code-countdown').hidden =
      (accessCodeExpiresIn_ > ACCESS_CODE_TIMER_DISPLAY_THRESHOLD_) ||
      !timerRunning_;
  return true;
}

/**
 * Update the text and appearance of the access code timeout element to
 * reflect the time remaining.
 */
function updateAccessCodeTimeoutElement_() {
  var pad = (accessCodeExpiresIn_ < 10) ? '0:0' : '0:';
  l10n.localizeElement(document.getElementById('seconds-remaining'),
                       pad + accessCodeExpiresIn_);
  if (!updateTimeoutStyles_()) {
    disableTimeoutCountdown_();
  }
}

/**
 * Callback to show or hide the NAT traversal warning when the policy changes.
 * @param {boolean} enabled True if NAT traversal is enabled.
 * @return {void} Nothing.
 */
function onNatTraversalPolicyChanged_(enabled) {
  var container = document.getElementById('nat-box-container');
  container.hidden = enabled;
}

}());
