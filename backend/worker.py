"""
Background Worker for Price Tracking
価格追跡用バックグラウンドワーカー
"""

import time

print("🔧 Worker starting...")

# Keep the worker running
while True:
    print("💓 Worker heartbeat...")
    time.sleep(60)
