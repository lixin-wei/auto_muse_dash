#include <ApplicationServices/ApplicationServices.h>
#include <Carbon/Carbon.h>
#include <chrono>
#include <iostream>
#include <thread>
#include <tuple>

inline uint64_t current_time_ms() {
  return std::chrono::duration_cast<std::chrono::milliseconds>(
             std::chrono::system_clock::now().time_since_epoch())
      .count();
}

inline void sleep_ms(uint64_t ms) {
  std::this_thread::sleep_for(std::chrono::milliseconds(ms));
}

std::tuple<uint8_t, uint8_t, uint8_t> GetScreenPixel(int x, int y) {
  CGRect rect;
  rect.origin.x = x;
  rect.origin.y = y;
  rect.size.height = 1;
  rect.size.width = 1;

  CGImageRef image_ref = CGDisplayCreateImageForRect(CGMainDisplayID(), rect);
  CFDataRef data_ref =
      CGDataProviderCopyData(CGImageGetDataProvider(image_ref));

  const uint8_t *buf = CFDataGetBytePtr(data_ref);

  auto tuple = std::make_tuple(buf[2], buf[1], buf[0]);

  CFRelease(data_ref);
  CGImageRelease(image_ref);
  return tuple;
}

void Press(int key, int duration_ms = 50) {
  // Create an HID hardware event source
  CGEventSourceRef src = CGEventSourceCreate(kCGEventSourceStateHIDSystemState);

  // Create a new keyboard key press event
  CGEventRef evt = CGEventCreateKeyboardEvent(src, (CGKeyCode)key, true);

  // Post keyboard event and release
  CGEventPost(kCGHIDEventTap, evt);
  CFRelease(evt);
  CFRelease(src);
  sleep_ms(duration_ms);
}

void Release(int key) {
  // Create an HID hardware event source
  CGEventSourceRef src = CGEventSourceCreate(kCGEventSourceStateHIDSystemState);

  // Create a new keyboard key release event
  CGEventRef evt = CGEventCreateKeyboardEvent(src, (CGKeyCode)key, false);

  // Post keyboard event and release
  CGEventPost(kCGHIDEventTap, evt);
  CFRelease(evt);
  CFRelease(src);
  sleep_ms(5);
}

void KeyClick(int key, int duration_ms) {
  Press(key, duration_ms);
  Release(key);
}

int main() {
  GetScreenPixel(497, 977);
  return 0;
}