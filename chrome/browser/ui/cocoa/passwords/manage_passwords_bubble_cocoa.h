// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#ifndef CHROME_BROWSER_UI_COCOA_PASSWORDS_MANAGE_PASSWORDS_BUBBLE_COCOA_H_
#define CHROME_BROWSER_UI_COCOA_PASSWORDS_MANAGE_PASSWORDS_BUBBLE_COCOA_H_

#import <Cocoa/Cocoa.h>

#include "base/mac/scoped_nsobject.h"
#import "chrome/browser/ui/passwords/manage_passwords_bubble.h"

namespace content {
class WebContents;
}

@class ManagePasswordsBubbleController;
@class ManagePasswordsBubbleCocoaNotificationBridge;

// Cocoa implementation of the platform-independent password bubble interface.
class ManagePasswordsBubbleCocoa : public ManagePasswordsBubble {
 public:
  // Creates and shows the bubble, which owns itself. Does nothing if the bubble
  // is already shown.
  static void ShowBubble(content::WebContents* webContents,
                         DisplayReason displayReason);

  // Closes and deletes the bubble.
  void Close();

  // Accessor for the global bubble.
  static ManagePasswordsBubbleCocoa* instance() { return bubble_; }

 private:
  friend class ManagePasswordsBubbleCocoaTest;

  // Instance-specific logic. Clients should use the static interface.
  ManagePasswordsBubbleCocoa(content::WebContents* webContents,
                             DisplayReason displayReason);
  virtual ~ManagePasswordsBubbleCocoa();
  void Show();

  // Cleans up state and deletes itself. Called when the bubble is closed.
  void OnClose();

  // Whether there is currently a close operation taking place. Prevents
  // multiple attempts to close the window.
  bool closing_;

  // The view controller for the bubble. Weak; owns itself. Must be nilled
  // after the bubble is closed.
  ManagePasswordsBubbleController* controller_;

  // WebContents on which the bubble should be displayed. Weak.
  content::WebContents* webContents_;

  // Listens for NSNotificationCenter notifications.
  base::scoped_nsobject<ManagePasswordsBubbleCocoaNotificationBridge> bridge_;

  // The global bubble instance. Deleted by Close().
  static ManagePasswordsBubbleCocoa* bubble_;

  DISALLOW_COPY_AND_ASSIGN(ManagePasswordsBubbleCocoa);
};

#endif  // CHROME_BROWSER_UI_COCOA_PASSWORDS_MANAGE_PASSWORDS_BUBBLE_COCOA_H_
