cam_width = 864
cam_height = 480
caught_lower_threshold = int(cam_height * 0.71)
speedy_caught_lower_threshold = int(cam_height * 0.55)
## Ball centering variables
offset = 0
center_x = cam_width / 2
center_y = cam_height / 2
threshold_x1 = center_x - int(cam_width / 100) + offset
threshold_x2 = center_x + int(cam_width / 100) + offset
ball_threshold_x1 = center_x - int(cam_width / 40) + offset
ball_threshold_x2 = center_x + int(cam_width / 40) + offset
toktok_threshold_x1 = center_x - int(cam_width / 5) + offset
toktok_threshold_x2 = center_x + int(cam_width / 5) + offset

ball_threshold_low = int(cam_height * 21 / 24)
ball_threshold_high = int(cam_height * 3 / 36)
basket_threshold_low = int(cam_height * 2 / 6)
