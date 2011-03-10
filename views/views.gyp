# Copyright (c) 2011 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
  'variables': {
    'chromium_code': 1,
  },

  'conditions': [
    [ 'OS=="linux" or OS=="freebsd" or OS=="openbsd"', {
      'conditions': [
        ['sysroot!=""', {
          'variables': {
            'pkg-config': './pkg-config-wrapper "<(sysroot)"',
          },
        }, {
          'variables': {
            'pkg-config': 'pkg-config'
          },
        }],]
    }],
  ],

  'target_defaults': {
    'sources/': [
      ['exclude', '/(cocoa|gtk|win)/'],
      ['exclude', '_(cocoa|gtk|linux|mac|posix|skia|win|x)\\.(cc|mm?)$'],
      ['exclude', '/(gtk|win|x11)_[^/]*\\.cc$'],
    ],
    'conditions': [
      ['OS=="linux" or OS=="freebsd" or OS=="openbsd"', {'sources/': [
        ['include', '/gtk/'],
        ['include', '_(gtk|linux|posix|skia|x)\\.cc$'],
        ['include', '/(gtk|x11)_[^/]*\\.cc$'],
      ]}],
      ['OS=="mac"', {'sources/': [
        ['include', '/cocoa/'],
        ['include', '_(cocoa|mac|posix)\\.(cc|mm?)$'],
      ]}, { # else: OS != "mac"
        'sources/': [
          ['exclude', '\\.mm?$'],
        ],
      }],
      ['OS=="win"', {'sources/': [
        ['include', '_(win)\\.cc$'],
        ['include', '/win/'],
        ['include', '/win_[^/]*\\.cc$'],
      ]}],
      ['touchui==0', {'sources/': [
        ['exclude', 'events/event_x.cc$'],
        ['exclude', 'ime/'],
        ['exclude', 'native_menu_x.cc$'],
        ['exclude', 'native_menu_x.h$'],
        ['exclude', 'touchui/'],
        ['exclude', '_(touch)\\.cc$'],
      ]}],
    ],
  },
  'targets': [
    {
      'target_name': 'views',
      'type': '<(library)',
      'msvs_guid': '6F9258E5-294F-47B2-919D-17FFE7A8B751',
      'dependencies': [
        '../app/app.gyp:app_base',
        '../app/app.gyp:app_resources',
        '../skia/skia.gyp:skia',
        '../third_party/icu/icu.gyp:icui18n',
        '../third_party/icu/icu.gyp:icuuc',
        '../ui/base/strings/ui_strings.gyp:ui_strings',
      ],
      'sources': [
        # All .cc, .h under views, except unittests
        'accelerator.cc',
        'accelerator.h',
        'accessibility/accessibility_types.h',
        'accessibility/view_accessibility.cc',
        'accessibility/view_accessibility.h',
        'animation/bounds_animator.cc',
        'animation/bounds_animator.h',
        'background.cc',
        'background.h',
        'border.cc',
        'border.h',
        'controls/button/button.cc',
        'controls/button/button.h',
        'controls/button/button_dropdown.cc',
        'controls/button/button_dropdown.h',
        'controls/button/checkbox.cc',
        'controls/button/checkbox.h',
        'controls/button/custom_button.cc',
        'controls/button/custom_button.h',
        'controls/button/image_button.cc',
        'controls/button/image_button.h',
        'controls/button/menu_button.cc',
        'controls/button/menu_button.h',
        'controls/button/native_button.cc',
        'controls/button/native_button.h',
        'controls/button/native_button_gtk.cc',
        'controls/button/native_button_gtk.h',
        'controls/button/native_button_win.cc',
        'controls/button/native_button_win.h',
        'controls/button/native_button_wrapper.h',
        'controls/button/radio_button.cc',
        'controls/button/radio_button.h',
        'controls/button/text_button.cc',
        'controls/button/text_button.h',
        'controls/combobox/combobox.cc',
        'controls/combobox/combobox.h',
        'controls/combobox/native_combobox_gtk.cc',
        'controls/combobox/native_combobox_gtk.h',
        'controls/combobox/native_combobox_win.cc',
        'controls/combobox/native_combobox_win.h',
        'controls/combobox/native_combobox_wrapper.h',
        'controls/image_view.cc',
        'controls/image_view.h',
        'controls/label.cc',
        'controls/label.h',
        'controls/link.cc',
        'controls/link.h',
        'controls/listbox/native_listbox_wrapper.h',
        'controls/listbox/native_listbox_win.cc',
        'controls/listbox/native_listbox_win.h',
        'controls/listbox/listbox.cc',
        'controls/listbox/listbox.h',
        'controls/menu/menu.cc',
        'controls/menu/menu.h',
        'controls/menu/menu_2.cc',
        'controls/menu/menu_2.h',
        'controls/menu/menu_config.cc',
        'controls/menu/menu_config.h',
        'controls/menu/menu_config_gtk.cc',
        'controls/menu/menu_config_win.cc',
        'controls/menu/menu_controller.cc',
        'controls/menu/menu_controller.h',
        'controls/menu/menu_delegate.cc',
        'controls/menu/menu_delegate.h',
        'controls/menu/menu_gtk.cc',
        'controls/menu/menu_gtk.h',
        'controls/menu/menu_host.h',
        'controls/menu/menu_host_root_view.cc',
        'controls/menu/menu_host_root_view.h',
        'controls/menu/menu_host_win.cc',
        'controls/menu/menu_host_win.h',
        'controls/menu/menu_host_gtk.cc',
        'controls/menu/menu_host_gtk.h',
        'controls/menu/menu_item_view.cc',
        'controls/menu/menu_item_view.h',
        'controls/menu/menu_item_view_gtk.cc',
        'controls/menu/menu_item_view_win.cc',
        'controls/menu/menu_scroll_view_container.cc',
        'controls/menu/menu_scroll_view_container.h',
        'controls/menu/menu_separator.h',
        'controls/menu/menu_separator_gtk.cc',
        'controls/menu/menu_separator_win.cc',
        'controls/menu/menu_win.cc',
        'controls/menu/menu_win.h',
        'controls/menu/menu_wrapper.h',
        'controls/menu/native_menu_gtk.cc',
        'controls/menu/native_menu_gtk.h',
        'controls/menu/native_menu_win.cc',
        'controls/menu/native_menu_win.h',
        'controls/menu/native_menu_x.cc',
        'controls/menu/native_menu_x.h',
        'controls/menu/nested_dispatcher_gtk.cc',
        'controls/menu/nested_dispatcher_gtk.h',
        'controls/menu/menu_image_util_gtk.cc',
        'controls/menu/menu_image_util_gtk.h',
        'controls/menu/submenu_view.cc',
        'controls/menu/submenu_view.h',
        'controls/menu/view_menu_delegate.h',
        'controls/message_box_view.cc',
        'controls/message_box_view.h',
        'controls/native_control.cc',
        'controls/native_control.h',
        'controls/native_control_gtk.cc',
        'controls/native_control_gtk.h',
        'controls/native_control_win.cc',
        'controls/native_control_win.h',
        'controls/native/native_view_host.cc',
        'controls/native/native_view_host.h',
        'controls/native/native_view_host_gtk.cc',
        'controls/native/native_view_host_gtk.h',
        'controls/native/native_view_host_win.cc',
        'controls/native/native_view_host_win.h',
        'controls/native/native_view_host_views.cc',
        'controls/native/native_view_host_views.h',
        'controls/native/native_view_host_wrapper.h',
        'controls/progress_bar.h',
        'controls/progress_bar.cc',
        'controls/resize_area.cc',
        'controls/resize_area.h',
        'controls/scroll_view.cc',
        'controls/scroll_view.h',
        'controls/scrollbar/bitmap_scroll_bar.cc',
        'controls/scrollbar/bitmap_scroll_bar.h',
        'controls/scrollbar/native_scroll_bar_gtk.cc',
        'controls/scrollbar/native_scroll_bar_gtk.h',
        'controls/scrollbar/native_scroll_bar_win.cc',
        'controls/scrollbar/native_scroll_bar_win.h',
        'controls/scrollbar/native_scroll_bar_wrapper.h',
        'controls/scrollbar/native_scroll_bar.cc',
        'controls/scrollbar/native_scroll_bar.h',
        'controls/scrollbar/scroll_bar.cc',
        'controls/scrollbar/scroll_bar.h',
        'controls/separator.cc',
        'controls/separator.h',
        'controls/single_split_view.cc',
        'controls/single_split_view.h',
        'controls/slider/slider.cc',
        'controls/slider/slider.h',
        'controls/slider/native_slider_gtk.cc',
        'controls/slider/native_slider_gtk.h',
        'controls/slider/native_slider_wrapper.h',
        'controls/tabbed_pane/tabbed_pane.cc',
        'controls/tabbed_pane/tabbed_pane.h',
        'controls/tabbed_pane/native_tabbed_pane_gtk.cc',
        'controls/tabbed_pane/native_tabbed_pane_gtk.h',
        'controls/tabbed_pane/native_tabbed_pane_win.cc',
        'controls/tabbed_pane/native_tabbed_pane_win.h',
        'controls/tabbed_pane/native_tabbed_pane_wrapper.h',
        'controls/table/native_table_wrapper.h',
        'controls/table/native_table_gtk.cc',
        'controls/table/native_table_gtk.h',
        'controls/table/native_table_win.cc',
        'controls/table/native_table_win.h',
        'controls/table/group_table_view.cc',
        'controls/table/group_table_view.h',
        'controls/table/table_view.cc',
        'controls/table/table_view.h',
        'controls/table/table_view2.cc',
        'controls/table/table_view2.h',
        'controls/table/table_view_observer.h',
        'controls/textfield/gtk_views_entry.cc',
        'controls/textfield/gtk_views_entry.h',
        'controls/textfield/gtk_views_textview.cc',
        'controls/textfield/gtk_views_textview.h',
        'controls/textfield/text_range.h',
        'controls/textfield/textfield.cc',
        'controls/textfield/textfield.h',
        'controls/textfield/textfield_controller.h',
        'controls/textfield/textfield_views_model.cc',
        'controls/textfield/textfield_views_model.h',
        'controls/textfield/native_textfield_gtk.cc',
        'controls/textfield/native_textfield_gtk.h',
        'controls/textfield/native_textfield_win.cc',
        'controls/textfield/native_textfield_win.h',
        'controls/textfield/native_textfield_wrapper.h',
        'controls/textfield/native_textfield_views.cc',
        'controls/textfield/native_textfield_views.h',
        'controls/throbber.cc',
        'controls/throbber.h',
        'controls/tree/tree_view.cc',
        'controls/tree/tree_view.h',
        #'debug_utils.cc',
        #'debug_utils.h',
        'drag_utils.cc',
        'drag_utils.h',
        'drag_utils_gtk.cc',
        'drag_utils_win.cc',
        'events/event.cc',
        'events/event.h',
        'events/event_gtk.cc',
        'events/event_win.cc',
        'events/event_utils_win.cc',
        'events/event_utils_win.h',
        'events/event_x.cc',
        'focus/accelerator_handler.h',
        'focus/accelerator_handler_gtk.cc',
        'focus/accelerator_handler_touch.cc',
        'focus/accelerator_handler_win.cc',
        'focus/external_focus_tracker.cc',
        'focus/external_focus_tracker.h',
        'focus/focus_manager_gtk.cc',
        'focus/focus_manager_win.cc',
        'focus/focus_manager.cc',
        'focus/focus_manager.h',
        'focus/focus_search.cc',
        'focus/focus_search.h',
        'focus/focus_util_win.cc',
        'focus/focus_util_win.h',
        'focus/view_storage.cc',
        'focus/view_storage.h',
        'ime/ibus_ime_context.cc',
        'ime/ime_context.cc',
        'ime/ime_context.h',
        'layout/box_layout.cc',
        'layout/box_layout.h',
        'layout/fill_layout.cc',
        'layout/fill_layout.h',
        'layout/grid_layout.cc',
        'layout/grid_layout.h',
        'layout/layout_constants.h',
        'layout/layout_manager.cc',
        'layout/layout_manager.h',
        'metrics.cc',
        'metrics.h',
        'metrics_gtk.cc',
        'metrics_win.cc',
        'mouse_watcher.cc',
        'mouse_watcher.h',
        'painter.cc',
        'painter.h',
        'repeat_controller.cc',
        'repeat_controller.h',
        'screen.h',
        'screen_gtk.cc',
        'screen_win.cc',
        'touchui/gesture_manager.cc',
        'touchui/gesture_manager.h',
        'touchui/touch_factory.cc',
        'touchui/touch_factory.h',
        'view.cc',
        'view.h',
        'view_constants.cc',
        'view_constants.h',
        'view_gtk.cc',
        'view_text_utils.cc',
        'view_text_utils.h',
        'view_win.cc',
        'views_delegate.h',
        'widget/aero_tooltip_manager.cc',
        'widget/aero_tooltip_manager.h',
        'widget/child_window_message_processor.cc',
        'widget/child_window_message_processor.h',
        'widget/default_theme_provider.cc',
        'widget/default_theme_provider.h',
        'widget/drop_helper.cc',
        'widget/drop_helper.h',
        'widget/drop_target_gtk.cc',
        'widget/drop_target_gtk.h',
        'widget/drop_target_win.cc',
        'widget/drop_target_win.h',
        'widget/gtk_views_fixed.cc',
        'widget/gtk_views_fixed.h',
        'widget/gtk_views_window.cc',
        'widget/gtk_views_window.h',
        'widget/root_view.cc',
        'widget/root_view.h',
        'widget/tooltip_manager_gtk.cc',
        'widget/tooltip_manager_gtk.h',
        'widget/tooltip_manager_win.cc',
        'widget/tooltip_manager_win.h',
        'widget/tooltip_manager.cc',
        'widget/tooltip_manager.h',
        'widget/tooltip_window_gtk.cc',
        'widget/tooltip_window_gtk.h',
        'widget/monitor_win.cc',
        'widget/monitor_win.h',
        'widget/native_widget.h',
        'widget/native_widget_delegate.h',
        'widget/widget.cc',
        'widget/widget.h',
        'widget/widget_gtk.cc',
        'widget/widget_gtk.h',
        'widget/widget_win.cc',
        'widget/widget_win.h',
        'window/client_view.cc',
        'window/client_view.h',
        'window/custom_frame_view.cc',
        'window/custom_frame_view.h',
        'window/dialog_client_view.cc',
        'window/dialog_client_view.h',
        'window/dialog_delegate.cc',
        'window/dialog_delegate.h',
        'window/native_frame_view.cc',
        'window/native_frame_view.h',
        'window/native_window.h',
        'window/native_window_delegate.h',
        'window/non_client_view.cc',
        'window/non_client_view.h',
        'window/window.cc',
        'window/window.h',
        'window/window_delegate.h',
        'window/window_delegate.cc',
        'window/window_resources.h',
        'window/window_gtk.cc',
        'window/window_gtk.h',
        'window/window_shape.cc',
        'window/window_shape.h',
        'window/window_win.cc',
        'window/window_win.h',
      ],
      'include_dirs': [
        '<(DEPTH)/third_party/wtl/include',
      ],
      'conditions': [
        ['OS=="linux" or OS=="freebsd" or OS=="openbsd"', {
          'dependencies': [
            '../build/linux/system.gyp:gtk',
            '../build/linux/system.gyp:x11',
            '../build/linux/system.gyp:xext',
          ],
          'sources!': [
            'accessibility/accessible_wrapper.cc',
            'accessibility/view_accessibility.cc',
            'accessibility/view_accessibility_wrapper.cc',
            'controls/scrollbar/bitmap_scroll_bar.cc',
            'controls/combo_box.cc',
            'controls/hwnd_view.cc',
            'controls/listbox/native_listbox_wrapper.h',
            'controls/listbox/listbox.cc',
            'controls/listbox/listbox.h',
            'controls/native_control.cc',
            'controls/table/group_table_view.cc',
            'controls/table/table_model.cc',
            'controls/table/table_view.cc',
            'controls/table/group_table_view.cc',
            'controls/tree/tree_view.cc',
            'events/event_win.cc',
            'resize_corner.cc',
            'widget/child_window_message_processor.cc',
            'widget/child_window_message_processor.h',
            'widget/aero_tooltip_manager.cc',
            'widget/root_view_drop_target.cc',
            'widget/widget_win.cc',
            'window/hit_test.cc',
            'window/native_frame_view.cc',
          ],
        }],
        ['touchui==1', {
          'dependencies': [
            '../build/linux/system.gyp:ibus',
          ],
          'defines': ['TOUCH_UI=1'],
          'sources/': [
            ['exclude', 'focus/accelerator_handler_gtk.cc'],
            ['exclude', 'controls/menu/native_menu_gtk.cc'],
          ],
          'conditions': [
            ['"<!@(<(pkg-config) --atleast-version=2.0 inputproto || echo $?)"!=""', {
              # Exclude TouchFactory if XInput2 is not available.
              'sources/': [
                ['exclude', 'touchui/touch_factory.cc'],
                ['exclude', 'touchui/touch_factory.h'],
              ],
            }],
            ['"<!@(<(pkg-config) --atleast-version=1.3.99 ibus-1.0 || echo $?)"!=""', {
              'sources/': [
                ['exclude', 'ime/ibus_ime_context.cc'],
              ],
              'defines': ['USE_DUMMY_IME_CONTEXT'],
            }],
          ],
        }],
        ['OS=="win"', {
          'sources!': [
            'controls/slider/slider.cc',
            'controls/slider/slider.h',
            'controls/slider/native_slider_wrapper.h',
          ],
          'include_dirs': [
            '<(DEPTH)/third_party/wtl/include',
          ],
        }],
      ],
    },
    {
      'target_name': 'views_unittests',
      'type': 'executable',
      'dependencies': [
        '../app/app.gyp:app_resources',
        '../base/base.gyp:base',
        '../base/base.gyp:test_support_base',
        '../skia/skia.gyp:skia',
        '../testing/gmock.gyp:gmock',
        '../testing/gtest.gyp:gtest',
        '../third_party/icu/icu.gyp:icui18n',
        '../third_party/icu/icu.gyp:icuuc',
        '../ui/base/strings/ui_strings.gyp:ui_strings',
        'views',
      ],
      'include_dirs': [
        '..',
      ],
      'sources': [
        'animation/bounds_animator_unittest.cc',
        'controls/label_unittest.cc',
        'controls/progress_bar_unittest.cc',
        'controls/single_split_view_unittest.cc',
        'controls/tabbed_pane/tabbed_pane_unittest.cc',
        'controls/table/table_view_unittest.cc',
        'controls/textfield/native_textfield_views_unittest.cc',
        'controls/textfield/textfield_views_model_unittest.cc',
        'focus/accelerator_handler_gtk_unittest.cc',
        'focus/focus_manager_unittest.cc',
        'layout/grid_layout_unittest.cc',
        'layout/box_layout_unittest.cc',
        'test/views_test_base.cc',
        'test/views_test_base.h',
        'run_all_unittests.cc',
        'test/test_views_delegate.cc',
        'test/test_views_delegate.h',
        'view_unittest.cc',
        'widget/native_widget_test_utils.h',
        'widget/native_widget_test_utils_gtk.cc',
        'widget/native_widget_test_utils_win.cc',
        'widget/native_widget_unittest.cc',
        'widget/widget_win_unittest.cc',
        'window/window_win_unittest.cc',

        '<(SHARED_INTERMEDIATE_DIR)/app/app_resources/app_resources.rc',
      ],
      'conditions': [
        ['OS=="linux" or OS=="freebsd" or OS=="openbsd"', {
          'dependencies': [
            '../build/linux/system.gyp:gtk',
            '../chrome/chrome.gyp:packed_resources',
          ],
          'conditions': [
            ['linux_use_tcmalloc==1', {
               'dependencies': [
                 '../base/allocator/allocator.gyp:allocator',
               ],
            }],
          ],
        },
        ],
        ['OS=="win"', {
          'dependencies': [
            # TODO(jcivelli): ideally the resource needed by views would be
            #                 factored out. (for some reason it pulls in a bunch
            #                 unrelated things like v8, sqlite nss...).
            '../chrome/app/locales/locales.gyp:en-US',
          ],
          'link_settings': {
            'libraries': [
              '-limm32.lib',
              '-loleacc.lib',
            ]
          },
          'include_dirs': [
            '<(DEPTH)/third_party/wtl/include',
          ],
        }],
      ],
    },
    {
      'target_name': 'views_examples',
      'type': 'executable',
      'dependencies': [
        '../base/base.gyp:base',
        '../skia/skia.gyp:skia',
        '../third_party/icu/icu.gyp:icui18n',
        '../third_party/icu/icu.gyp:icuuc',
        'views',
      ],
      'include_dirs': [
        '..',
      ],
      'sources': [
        'examples/button_example.cc',
        'examples/button_example.h',
        'examples/combobox_example.cc',
        'examples/combobox_example.h',
        'examples/example_base.cc',
        'examples/example_base.h',
        'examples/examples_main.cc',
        'examples/examples_main.h',
        'examples/message_box_example.cc',
        'examples/message_box_example.h',
        'examples/menu_example.cc',
        'examples/menu_example.h',
        'examples/radio_button_example.cc',
        'examples/radio_button_example.h',
        'examples/scroll_view_example.cc',
        'examples/scroll_view_example.h',
        'examples/single_split_view_example.cc',
        'examples/single_split_view_example.h',
        'examples/slider_example.cc',
        'examples/slider_example.h',
        'examples/tabbed_pane_example.cc',
        'examples/tabbed_pane_example.h',
        'examples/table2_example.cc',
        'examples/table2_example.h',
        'examples/textfield_example.cc',
        'examples/textfield_example.h',
        'examples/throbber_example.cc',
        'examples/throbber_example.h',
        'examples/widget_example.cc',
        'examples/widget_example.h',

        '<(SHARED_INTERMEDIATE_DIR)/app/app_resources/app_resources.rc',
      ],
      'conditions': [
        ['OS=="linux" or OS=="freebsd" or OS=="openbsd"', {
          'dependencies': [
            '../build/linux/system.gyp:gtk',
            '../chrome/chrome.gyp:packed_resources',
          ],
          'conditions': [
            ['linux_use_tcmalloc==1', {
               'dependencies': [
                 '../base/allocator/allocator.gyp:allocator',
               ],
            }],
          ],
        },
        ],
        ['OS=="win"', {
          'link_settings': {
            'libraries': [
              '-limm32.lib',
              '-loleacc.lib',
            ]
          },
          'include_dirs': [
            '<(DEPTH)/third_party/wtl/include',
          ],
        }],
      ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
