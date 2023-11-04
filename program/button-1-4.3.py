import lvgl as lv
import lv_utils
import tft_config
from xpt2046 import Touch
from machine import SPI, Pin
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


class CounterBtn():
    def __init__(self, scr):
        self.cnt = 0
        btn = lv.btn(scr)
        btn.set_size(120, 50)
        btn.align(lv.ALIGN.CENTER,0,0)
        btn.add_event_cb(self.btn_event_cb, lv.EVENT.ALL, None)
        label = lv.label(btn)
        label.set_text("Button")
        label.center()

    def btn_event_cb(self, evt):
        code = evt.get_code()
        btn = evt.get_target()
        if code == lv.EVENT.CLICKED:
            self.cnt += 1


        label = btn.get_child(0)
        label.set_text("Button: " + str(self.cnt))


counterBtn = CounterBtn(scr)
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
