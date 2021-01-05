import cv2
import winsound

cam = cv2.VideoCapture(0)
while cam.isOpened():
    ret1, frame1 = cam.read()
    frame1 = cv2.flip(frame1, 1)                                    # Inverse frame 1
    ret2, frame2 = cam.read()
    frame2 = cv2.flip(frame2, 1)                                    # Inverse frame 2

    diff = cv2.absdiff(frame1, frame2)                              # Capturing two instance and comparing
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)                   # Using single gray color
    blur = cv2.GaussianBlur(gray, (5, 5), 0)                        # Blur the gray
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)     # Remove the noise

    dilated = cv2.dilate(thresh, None, iterations=3)                # Make the interested things interesting

    # Boundary for moving objects
    _, contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours (frame,contours,index,color,thickness)
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    # if and only if the movement is large & form a rectangle
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        # frame, axis, width, height, color, thickness
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Beep(frequency, duration)
        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

    if cv2.waitKey(10) == ord('q'):
        break

    cv2.imshow('Spy Cam', frame1)                                   # Draw frame 1
