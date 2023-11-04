import lvgl as lv
import lv_utils
import tft_config
from xpt2046 import Touch
import fs_driver
from machine import Pin,ADC,SPI
import onewire, ds18x20
import time

WIDTH = 480
HEIGHT = 272

# tft drvier
tft = tft_config.config()

# touch drvier
spi = SPI(2, baudrate=1000000)
spi.init(sck=Pin(12), mosi=Pin(11), miso=Pin(13))
cs = Pin(0, mode=Pin.OUT, value=1)
int_pin = Pin(36)
xpt = Touch(spi, cs=cs, int_pin=int_pin)
xmin = 96
xmax = 1951
ymin = 175
ymax = 1908
orientation = 0
xpt.calibrate(xmin, xmax, ymin, ymax, 480, 272, orientation)

lv.init()

if not lv_utils.event_loop.is_running():
    event_loop=lv_utils.event_loop()
    print(event_loop.is_running())

# create a display 0 buffer
disp_buf0 = lv.disp_draw_buf_t()
buf1_0 = bytearray(WIDTH * 10)
disp_buf0.init(buf1_0, None, len(buf1_0) // lv.color_t.__SIZE__)

# register display driver
disp_drv = lv.disp_drv_t()
disp_drv.init()
disp_drv.draw_buf = disp_buf0
disp_drv.flush_cb = tft.flush
disp_drv.hor_res = WIDTH
disp_drv.ver_res = HEIGHT
# disp_drv.user_data = {"swap": 0}
disp0 = disp_drv.register()
lv.disp_t.set_default(disp0)

# touch driver init
indev_drv = lv.indev_drv_t()
indev_drv.init()
indev_drv.disp = disp0
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = xpt.read
indev = indev_drv.register()

scr = lv.obj()
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')
scr = lv.scr_act()
scr.clean()
ps2_y = ADC(Pin(18))
ps2_y.atten(ADC.ATTN_11DB)
s = 0
pin16 = Pin(38, Pin.OUT)

class MyWidget():
    def __init__(self, scr):

        self.meter = lv.meter(scr)
        self.meter.set_pos(20, 50)

        self.meter.set_size(200, 200)

        label = lv.label(self.meter)
        label.set_text("Light intensity")
        label.align( lv.ALIGN.CENTER, 0, 75)


        scale = self.meter.add_scale()

        self.meter.set_scale_ticks(scale, 51, 2, 10, lv.palette_main(lv.PALETTE.GREY))

        self.meter.set_scale_major_ticks(scale, 10, 4, 15, lv.color_black(), 20)


        blue_arc = self.meter.add_arc(scale, 2, lv.palette_main(lv.PALETTE.BLUE), 0)
        self.meter.set_indicator_start_value(blue_arc, 0)
        self.meter.set_indicator_end_value(blue_arc, 100)


        blue_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.BLUE), False, 0)
        self.meter.set_indicator_start_value(blue_arc_scale, 0)
        self.meter.set_indicator_end_value(blue_arc_scale, 20)


        red_arc = self.meter.add_arc(scale, 2, lv.palette_main(lv.PALETTE.RED), 0)
        self.meter.set_indicator_start_value(red_arc, 80)
        self.meter.set_indicator_end_value(red_arc, 100)


        red_arc_scale = self.meter.add_scale_lines(scale, lv.palette_main(lv.PALETTE.RED), lv.palette_main(lv.PALETTE.RED), False, 0)
        self.meter.set_indicator_start_value(red_arc_scale, 80)
        self.meter.set_indicator_end_value(red_arc_scale, 100)


        self.indic = self.meter.add_needle_line(scale, 4, lv.palette_main(lv.PALETTE.GREY), -10)


        a = lv.anim_t()
        a.init()
        a.set_var(self.indic)
        val_y = ps2_y.read()
        a.set_values(0, 100)
        a.set_time(2000)
        a.set_repeat_delay(100)
        a.set_playback_time(500)
        a.set_playback_delay(100)
        a.set_repeat_count(lv.ANIM_REPEAT.INFINITE)
        a.set_custom_exec_cb(self.set_value)
        lv.anim_t.start(a)

    def set_value(self, anmi_obj, value):
        ps2_y = ADC(Pin(18))
        ps2_y_value = ps2_y.read()
        ps2_y = int(ps2_y_value)
        s = int((((ps2_y - 0) * 100) / 4095) + 0)
        if s > 60:
            pin16.value(0)
            label2.set_text(" ")
            label3.set_text("OFF")
        else:
            pin16.value(1)
            label2.set_text("ON")
            label3.set_text(" ")
        self.meter.set_indicator_value(self.indic, s)

btn2 = lv.btn(scr)
btn2.set_size(40, 30)
btn2.align(lv.ALIGN.CENTER,50,0)
style_btn2 = lv.style_t()
style_btn2.init()
style_btn2.set_bg_color(lv.color_hex(0x00FF00))

label2 = lv.label(btn2)
label2.set_text("ON")
label2.center()

btn3 = lv.btn(scr)
btn3.set_size(40, 30)
btn3.align(lv.ALIGN.CENTER,100,0)
style_btn3 = lv.style_t()
style_btn3.init()

style_btn3.set_bg_color(lv.color_hex(0xFFFF00))

label3 = lv.label(btn3)
label3.set_text("OFF")
label3.center()


MyWidget(scr)


lv.scr_load(scr)



try:
    from machine import WDT
    wdt = WDT(timeout=1000)  # enable it with a timeout of 2s
    print("Hint: Press Ctrl+C to end the program")
    while True:
        wdt.feed()
        time.sleep(0.9)
except KeyboardInterrupt as ret:
    print("The program stopped running, ESP32 has restarted...")
    time.sleep(10)


