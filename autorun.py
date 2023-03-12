from pynput.mouse import Listener
import time
import macos_native_tools as mac_tools
import os

click_x = 0
click_y = 0
def get_click_point():
    def on_click(x, y, button, pressed):
        # print(f"x:{x}, y:{y}, button:{button}, pressed:{pressed}")
        global click_x, click_y
        click_x = x
        click_y = y
        if pressed:
            return False
    with Listener(on_click=on_click) as listener:
        listener.join()
        return (click_x, click_y)


# Ask user to get the stroke point
# print("Please click the center of the air strike point...")
# air_point = get_click_point()
# print("Please click the center of the floor strike point...")
# floor_point = get_click_point()

air_point = (131.98828125, 176.70703125)
floor_point = (131.6875, 277.32421875)

print(f"air point:{air_point}, floor point:{floor_point}")


# Monitor the color of the two points:
strike_colors=[
    # air ---
    (104, 219, 251), # blue cat
    (46, 80, 229), # blue notes
    (78,169,248), (117,251,248),
    # both
    (252,241,80),
    # floor ------
    (253, 243, 179), # yellow cloud
    (234,51,159),
    (235,89,192),
]

gear_colors = [(221, 254, 244), (108,229,249), (97,198,250), (155, 101, 212)]
gear_detect_point = (195, 310)

def color_diff(c1, c2):
    return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]) + abs(c1[2]-c2[2])


def get_screen_pixel(p):
    return mac_tools.get_screen_pixel(int(p[0]), int(p[1]))


def run_song(song_len_second):
    start_time = time.time()
    loop_count = 0
    last_log_time = start_time
    while True:
        color_air = get_screen_pixel(air_point)
        color_floor = get_screen_pixel(floor_point)
        color_gear_point = get_screen_pixel(gear_detect_point)
        # print(f"air color:{color_air}, floor color:{color_floor}")

        DIFF_TOLERANCE = 30
        # Detect gears
        min_diff = 999;
        for color in gear_colors:
            if color_diff(color_gear_point, color) < DIFF_TOLERANCE:
                mac_tools.key_click(mac_tools.key_code_f, 800)
                break

        # Detect enemies
        strike_air = False
        strike_floor = False
        for color in strike_colors:
            if color_diff(color, color_air) < DIFF_TOLERANCE:
                strike_air = True
            if color_diff(color, color_floor) < DIFF_TOLERANCE:
                strike_floor = True
            if strike_floor or strike_air:
                break
        
        if strike_air and strike_floor:
            # decrease press duration in order not to block floor strike
            mac_tools.key_click(mac_tools.key_code_f, 1)
            mac_tools.key_click(mac_tools.key_code_j)
        elif strike_air:
            mac_tools.key_click(mac_tools.key_code_f)
        elif strike_floor:
            mac_tools.key_click(mac_tools.key_code_j)

        # calculate sample rate
        now = time.time()
        time_passed = now - start_time
        if time_passed > song_len_second:
            break
        loop_count += 1
        time_since_last_log = now - last_log_time
        if time_since_last_log > 1:
            last_log_time = now
            sample_rate = loop_count/time_since_last_log
            print(f"Sample rate: {sample_rate} fps")
            loop_count = 0
        time.sleep(0.001)


def press_enter():
    mac_tools.key_click(mac_tools.key_code_return, 500)


# wait user to switch to game window
print("Please switch to game window")
time.sleep(5)
round_cnt = 0
while True:
    round_cnt += 1
    print(f"Round {round_cnt}")
    # enter song
    for _ in range(4):
        press_enter()
        time.sleep(1)
    # run!
    # run_song(134 + 20)
    run_song(90 + 20)
    # to main menu
    press_enter()
    # wait until main menu
    time.sleep(10)