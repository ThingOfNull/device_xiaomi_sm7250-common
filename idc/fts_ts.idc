# Input Device Configuration for Focaltech FTS touchscreen
# Device name from EventHub: "fts_ts"
#
# enableForInactiveViewport: Keep touch mapper active even when the display
# viewport is marked as inactive. Without this, Android 16's SurfaceFlinger
# idle mechanism can cause the viewport to briefly go inactive, which disables
# the touch mapper and causes ~400ms input latency on first touch after idle.

touch.enableForInactiveViewport = 1
