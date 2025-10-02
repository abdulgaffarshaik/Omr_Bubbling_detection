import cv2
import csv

# Load image
image = cv2.imread("A:\csv\image.jpg")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Blur and Threshold
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(
    blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)

# Find contours
contours, _ = cv2.findContours(
    thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

bubbles = []

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    # Filter bubbles by size
    if 20 < w < 50 and 20 < h < 50:
        roi = thresh[y:y+h, x:x+w]
        white = cv2.countNonZero(roi)
        total = w * h
        fill_ratio = white / float(total)

        if fill_ratio > 0.4:  # Considered filled
            cx = x + w // 2
            cy = y + h // 2
            bubbles.append((cx, cy, fill_ratio))

if not bubbles:
    print("No bubbles detected!")

else:
    # Sort bubbles left-right
    bubbles.sort(key=lambda b: b[0])
    mid_x = (bubbles[0][0] + bubbles[-1][0]) // 2

    left_bubbles = [b for b in bubbles if b[0] < mid_x]
    right_bubbles = [b for b in bubbles if b[0] > mid_x]

    def detect_digit(col_bubbles):
        if not col_bubbles:
            return None
        # Sort top-to-bottom
        col_bubbles.sort(key=lambda b: b[1])
        n = len(col_bubbles)
        detected = []
        for i, b in enumerate(col_bubbles):
            # Map position to digit (0–9)
            digit = round((i / (n - 1)) * 9) if n > 1 else 0
            detected.append((digit, b[2]))
        # Pick bubble with max fill ratio
        return max(detected, key=lambda d: d[1])[0]

    left_digit = detect_digit(left_bubbles)
    right_digit = detect_digit(right_bubbles)

    print(f"Left column: {left_digit}")
    print(f"Right column: {right_digit}")

    if left_digit is not None and right_digit is not None:
        Total = left_digit * 10 + right_digit
        print(f"Total: {Total}")
    else:
        final_number = None
        print("Could not detect final number")

    # Save results to CSV
    with open("bubbled_result.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Left", "Right", "Total"])
        writer.writerow([left_digit, right_digit, Total])
