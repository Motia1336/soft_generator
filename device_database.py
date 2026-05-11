# device_database.py
import random

def generate_database():
    # --- IOS DEVICES (Static Specs) ---
    # (model_name, launch_os, width, height, cpu, ram, renderer)
    ios_base = [
        ("iPhone XR", 12, 828, 1792, 6, 3, "Apple A12 GPU"),
        ("iPhone XS", 12, 1125, 2436, 6, 4, "Apple A12 GPU"),
        ("iPhone XS Max", 12, 1242, 2688, 6, 4, "Apple A12 GPU"),
        ("iPhone 11", 13, 828, 1792, 6, 4, "Apple A13 GPU"),
        ("iPhone 11 Pro", 13, 1125, 2436, 6, 4, "Apple A13 GPU"),
        ("iPhone 11 Pro Max", 13, 1242, 2688, 6, 4, "Apple A13 GPU"),
        ("iPhone SE (2nd gen)", 13, 750, 1334, 6, 3, "Apple A13 GPU"),
        ("iPhone 12 mini", 14, 1080, 2340, 6, 4, "Apple A14 GPU"),
        ("iPhone 12", 14, 1170, 2532, 6, 4, "Apple A14 GPU"),
        ("iPhone 12 Pro", 14, 1170, 2532, 6, 6, "Apple A14 GPU"),
        ("iPhone 12 Pro Max", 14, 1284, 2778, 6, 6, "Apple A14 GPU"),
        ("iPhone 13 mini", 15, 1080, 2340, 6, 4, "Apple A15 GPU"),
        ("iPhone 13", 15, 1170, 2532, 6, 4, "Apple A15 GPU"),
        ("iPhone 13 Pro", 15, 1170, 2532, 6, 6, "Apple A15 GPU"),
        ("iPhone 13 Pro Max", 15, 1284, 2778, 6, 6, "Apple A15 GPU"),
        ("iPhone SE (3rd gen)", 15, 750, 1334, 6, 4, "Apple A15 GPU"),
        ("iPhone 14", 16, 1170, 2532, 6, 6, "Apple A15 GPU"),
        ("iPhone 14 Plus", 16, 1284, 2778, 6, 6, "Apple A15 GPU"),
        ("iPhone 14 Pro", 16, 1179, 2556, 6, 6, "Apple A16 GPU"),
        ("iPhone 14 Pro Max", 16, 1290, 2796, 6, 6, "Apple A16 GPU"),
        ("iPhone 15", 17, 1179, 2556, 6, 6, "Apple A16 GPU"),
        ("iPhone 15 Plus", 17, 1290, 2796, 6, 6, "Apple A16 GPU"),
        ("iPhone 15 Pro", 17, 1179, 2556, 6, 8, "Apple A17 Pro GPU"),
        ("iPhone 15 Pro Max", 17, 1290, 2796, 6, 8, "Apple A17 Pro GPU"),
        ("iPhone 16", 18, 1179, 2556, 6, 8, "Apple A18 GPU"),
        ("iPhone 16 Plus", 18, 1290, 2796, 6, 8, "Apple A18 GPU"),
        ("iPhone 16 Pro", 18, 1206, 2622, 6, 8, "Apple A18 Pro GPU"),
        ("iPhone 16 Pro Max", 18, 1320, 2868, 6, 8, "Apple A18 Pro GPU"),
        ("iPhone 17", 26, 1179, 2556, 6, 8, "Apple A19 GPU"),
        ("iPhone 17 Air", 26, 1290, 2796, 6, 8, "Apple A19 GPU"),
        ("iPhone 17 Pro", 26, 1206, 2622, 6, 12, "Apple A19 Pro GPU"),
        ("iPhone 17 Pro Max", 26, 1320, 2868, 6, 12, "Apple A19 Pro GPU"),
    ]
    
    def get_cams(brand, model):
        model_lower = model.lower()
        if brand == "Apple":
            if "se" in model_lower: return 2
            if "pro" in model_lower: return 4
            return 3 # standard iphones have 2 back + 1 front = 3 (XR has 1+1=2 but 3 is safer average)
        else:
            if "ultra" in model_lower or "pro+" in model_lower: return 5
            if "pro" in model_lower or "fold" in model_lower or "flip" in model_lower: return 4
            return 3 # standard androids have 2 back + 1 front = 3

    ios_final = []
    for model in ios_base:
        cams = get_cams("Apple", model[0])
        ios_final.append(("Apple", model[0], str(model[1]), model[2], model[3], model[4], model[5], 3, 2, cams, "Apple Inc.", model[6]))
    
    # --- ANDROID DEVICES (Static Specs for every model) ---
    # format: (Brand, Model, LaunchOS, W, H, CPU, RAM, Vendor, Renderer)
    android_raw_data = [
        # Samsung
        ("Samsung", "Galaxy S10", 9.0, 1440, 3040, 8, 8, "Qualcomm", "Adreno 640"),
        ("Samsung", "Galaxy Note 10", 9.0, 1080, 2280, 8, 8, "Qualcomm", "Adreno 640"),
        ("Samsung", "Galaxy S20", 10.0, 1440, 3200, 8, 8, "Qualcomm", "Adreno 650"),
        ("Samsung", "Galaxy Note 20 Ultra", 10.0, 1440, 3088, 8, 12, "Qualcomm", "Adreno 650"),
        ("Samsung", "Galaxy A52", 11.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 619"),
        ("Samsung", "Galaxy S21", 11.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 660"),
        ("Samsung", "Galaxy Z Fold 3", 11.0, 1768, 2208, 8, 12, "Qualcomm", "Adreno 660"),
        ("Samsung", "Galaxy S22", 12.0, 1080, 2340, 8, 8, "Qualcomm", "Adreno 730"),
        ("Samsung", "Galaxy A53", 12.0, 1080, 2400, 8, 6, "Samsung", "Mali-G68"),
        ("Samsung", "Galaxy Z Flip 4", 12.0, 1080, 2640, 8, 8, "Qualcomm", "Adreno 730"),
        ("Samsung", "Galaxy S23", 13.0, 1080, 2340, 8, 8, "Qualcomm", "Adreno 740"),
        ("Samsung", "Galaxy A54", 13.0, 1080, 2340, 8, 8, "Samsung", "Mali-G68"),
        ("Samsung", "Galaxy Z Fold 5", 13.0, 1812, 2176, 8, 12, "Qualcomm", "Adreno 740"),
        ("Samsung", "Galaxy S24 Ultra", 14.0, 1440, 3120, 8, 12, "Qualcomm", "Adreno 750"),
        ("Samsung", "Galaxy A55", 14.0, 1080, 2340, 8, 8, "Samsung", "Xclipse 530"),
        ("Samsung", "Galaxy Z Flip 6", 14.0, 1080, 2640, 8, 12, "Qualcomm", "Adreno 750"),
        # Google
        ("Google", "Pixel 3", 9.0, 1080, 2160, 8, 4, "Qualcomm", "Adreno 630"),
        ("Google", "Pixel 3a", 9.0, 1080, 2220, 8, 4, "Qualcomm", "Adreno 615"),
        ("Google", "Pixel 4", 10.0, 1080, 2280, 8, 6, "Qualcomm", "Adreno 640"),
        ("Google", "Pixel 4a", 10.0, 1080, 2340, 8, 6, "Qualcomm", "Adreno 618"),
        ("Google", "Pixel 5", 11.0, 1080, 2340, 8, 8, "Qualcomm", "Adreno 620"),
        ("Google", "Pixel 5a", 11.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 620"),
        ("Google", "Pixel 6", 12.0, 1080, 2400, 8, 8, "Google", "Mali-G78"),
        ("Google", "Pixel 6 Pro", 12.0, 1440, 3120, 8, 12, "Google", "Mali-G78"),
        ("Google", "Pixel 6a", 12.0, 1080, 2400, 8, 6, "Google", "Mali-G78"),
        ("Google", "Pixel 7", 13.0, 1080, 2400, 8, 8, "Google", "Mali-G710"),
        ("Google", "Pixel 7 Pro", 13.0, 1440, 3120, 8, 12, "Google", "Mali-G710"),
        ("Google", "Pixel 7a", 13.0, 1080, 2400, 8, 8, "Google", "Mali-G710"),
        ("Google", "Pixel 8", 14.0, 1080, 2400, 8, 8, "Google", "Mali-G715"),
        ("Google", "Pixel 8 Pro", 14.0, 1344, 2992, 8, 12, "Google", "Mali-G715"),
        ("Google", "Pixel 8a", 14.0, 1080, 2400, 8, 8, "Google", "Mali-G715"),
        ("Google", "Pixel 9", 15.0, 1080, 2424, 8, 12, "Google", "Mali-G715"),
        ("Google", "Pixel 9 Pro", 15.0, 1280, 2856, 8, 16, "Google", "Mali-G715"),
        ("Google", "Pixel 9 Pro Fold", 15.0, 2076, 2152, 8, 16, "Google", "Mali-G715"),
        ("Google", "Pixel 9a", 15.0, 1080, 2400, 8, 8, "Google", "Mali-G715"),
        ("Google", "Pixel Fold", 13.0, 1840, 2208, 8, 12, "Google", "Mali-G710"),
        # Xiaomi
        ("Xiaomi", "Mi 9", 9.0, 1080, 2340, 8, 6, "Qualcomm", "Adreno 640"),
        ("Xiaomi", "Redmi Note 8 Pro", 9.0, 1080, 2340, 8, 6, "ARM", "Mali-G76"),
        ("Xiaomi", "Mi 10", 10.0, 1080, 2340, 8, 8, "Qualcomm", "Adreno 650"),
        ("Xiaomi", "Redmi Note 10 Pro", 11.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 618"),
        ("Xiaomi", "Mi 11", 11.0, 1440, 3200, 8, 8, "Qualcomm", "Adreno 660"),
        ("Xiaomi", "Xiaomi 11T Pro", 11.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 660"),
        ("Xiaomi", "Redmi Note 11 Pro", 11.0, 1080, 2400, 8, 6, "MediaTek", "Mali-G57"),
        ("Xiaomi", "Xiaomi 12", 12.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 730"),
        ("Xiaomi", "Redmi Note 12 Pro", 12.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G68"),
        ("Xiaomi", "Xiaomi 13", 13.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 740"),
        ("Xiaomi", "Redmi Note 13 Pro", 13.0, 1220, 2712, 8, 8, "Qualcomm", "Adreno 710"),
        ("Xiaomi", "Xiaomi 14", 14.0, 1200, 2670, 8, 8, "Qualcomm", "Adreno 750"),
        ("Xiaomi", "Xiaomi 14 Ultra", 14.0, 1440, 3200, 8, 12, "Qualcomm", "Adreno 750"),
        ("Xiaomi", "Redmi Note 14 Pro", 14.0, 1220, 2712, 8, 8, "MediaTek", "Mali-G615"),
        # Poco
        ("Poco", "Poco F2 Pro", 10.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 650"),
        ("Poco", "Poco X3 NFC", 10.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 618"),
        ("Poco", "Poco M3", 10.0, 1080, 2340, 8, 4, "Qualcomm", "Adreno 610"),
        ("Poco", "Poco F3", 11.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 650"),
        ("Poco", "Poco X3 Pro", 11.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 640"),
        ("Poco", "Poco M4 Pro", 11.0, 1080, 2400, 8, 6, "MediaTek", "Mali-G57"),
        ("Poco", "Poco F4", 12.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 650"),
        ("Poco", "Poco X4 Pro 5G", 11.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 619"),
        ("Poco", "Poco M5", 12.0, 1080, 2408, 8, 4, "MediaTek", "Mali-G57"),
        ("Poco", "Poco F5", 13.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 725"),
        ("Poco", "Poco X5 Pro", 12.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 642L"),
        ("Poco", "Poco M6 Pro", 13.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G57"),
        ("Poco", "Poco F6", 14.0, 1220, 2712, 8, 8, "Qualcomm", "Adreno 735"),
        ("Poco", "Poco X6 Pro", 14.0, 1220, 2712, 8, 8, "MediaTek", "Mali-G615"),
        ("Poco", "Poco M7 Pro", 14.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G610"),
        # Realme
        ("Realme", "Realme 3 Pro", 9.0, 1080, 2340, 8, 4, "Qualcomm", "Adreno 616"),
        ("Realme", "Realme X2 Pro", 9.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 640"),
        ("Realme", "Realme 6 Pro", 10.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 618"),
        ("Realme", "Realme 7 Pro", 10.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 618"),
        ("Realme", "Realme 8 Pro", 11.0, 1080, 2400, 8, 6, "Qualcomm", "Adreno 618"),
        ("Realme", "Realme GT 5G", 11.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 660"),
        ("Realme", "Realme 9 Pro+", 12.0, 1080, 2400, 8, 6, "MediaTek", "Mali-G68"),
        ("Realme", "Realme GT Neo 3", 12.0, 1080, 2412, 8, 8, "MediaTek", "Mali-G610"),
        ("Realme", "Realme 10 Pro+", 13.0, 1080, 2412, 8, 8, "MediaTek", "Mali-G68"),
        ("Realme", "Realme GT3", 13.0, 1240, 2772, 8, 16, "Qualcomm", "Adreno 730"),
        ("Realme", "Realme 11 Pro+", 13.0, 1080, 2412, 8, 8, "MediaTek", "Mali-G68"),
        ("Realme", "Realme GT5", 13.0, 1240, 2772, 8, 12, "Qualcomm", "Adreno 730"),
        ("Realme", "Realme 12 Pro+", 14.0, 1080, 2412, 8, 8, "Qualcomm", "Adreno 710"),
        ("Realme", "Realme GT5 Pro", 14.0, 1264, 2780, 8, 12, "Qualcomm", "Adreno 750"),
        ("Realme", "Realme 13 Pro+", 14.0, 1080, 2412, 8, 12, "Qualcomm", "Adreno 710"),
        # Oppo
        ("Oppo", "Reno 2", 9.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 618"),
        ("Oppo", "Find X2 Pro", 10.0, 1440, 3168, 8, 12, "Qualcomm", "Adreno 650"),
        ("Oppo", "Reno 4 Pro", 10.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 620"),
        ("Oppo", "Find X3 Pro", 11.0, 1440, 3216, 8, 12, "Qualcomm", "Adreno 660"),
        ("Oppo", "Reno 6 Pro", 11.0, 1080, 2400, 8, 12, "MediaTek", "Mali-G77"),
        ("Oppo", "Find X5 Pro", 12.0, 1440, 3216, 8, 12, "Qualcomm", "Adreno 730"),
        ("Oppo", "Reno 8 Pro", 12.0, 1080, 2412, 8, 8, "MediaTek", "Mali-G610"),
        ("Oppo", "Find N2 Flip", 13.0, 1080, 2520, 8, 8, "MediaTek", "Mali-G710"),
        ("Oppo", "Find X6 Pro", 13.0, 1440, 3168, 8, 12, "Qualcomm", "Adreno 740"),
        ("Oppo", "Reno 10 Pro", 13.0, 1080, 2412, 8, 12, "Qualcomm", "Adreno 642L"),
        ("Oppo", "Find N3", 13.0, 2268, 2440, 8, 12, "Qualcomm", "Adreno 740"),
        ("Oppo", "Find X7 Ultra", 14.0, 1440, 3168, 8, 12, "Qualcomm", "Adreno 750"),
        ("Oppo", "Reno 11 Pro", 14.0, 1080, 2412, 8, 12, "MediaTek", "Mali-G610"),
        # Vivo
        ("Vivo", "V15 Pro", 9.0, 1080, 2340, 8, 6, "Qualcomm", "Adreno 612"),
        ("Vivo", "X50 Pro", 10.0, 1080, 2376, 8, 8, "Qualcomm", "Adreno 620"),
        ("Vivo", "V20", 11.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 618"),
        ("Vivo", "X60 Pro", 11.0, 1080, 2376, 8, 12, "Qualcomm", "Adreno 650"),
        ("Vivo", "V21", 11.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G57"),
        ("Vivo", "X70 Pro", 11.0, 1080, 2376, 8, 8, "MediaTek", "Mali-G78"),
        ("Vivo", "V23", 12.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G68"),
        ("Vivo", "X80 Pro", 12.0, 1440, 3200, 8, 12, "Qualcomm", "Adreno 730"),
        ("Vivo", "V25", 12.0, 1080, 2404, 8, 8, "MediaTek", "Mali-G68"),
        ("Vivo", "X90 Pro", 13.0, 1260, 2800, 8, 12, "MediaTek", "Mali-G715"),
        ("Vivo", "V27", 13.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G610"),
        ("Vivo", "X100 Pro", 14.0, 1260, 2800, 8, 12, "MediaTek", "Mali-G720"),
        ("Vivo", "V29", 14.0, 1260, 2800, 8, 8, "Qualcomm", "Adreno 642L"),
        ("Vivo", "X Fold 3", 14.0, 2200, 2480, 8, 16, "Qualcomm", "Adreno 750"),
        # OnePlus
        ("OnePlus", "OnePlus 6", 8.1, 1080, 2280, 8, 6, "Qualcomm", "Adreno 630"),
        ("OnePlus", "OnePlus 6T", 9.0, 1080, 2340, 8, 6, "Qualcomm", "Adreno 630"),
        ("OnePlus", "OnePlus 7 Pro", 9.0, 1440, 3120, 8, 8, "Qualcomm", "Adreno 640"),
        ("OnePlus", "OnePlus 7T", 10.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 640"),
        ("OnePlus", "OnePlus 8 Pro", 10.0, 1440, 3168, 8, 8, "Qualcomm", "Adreno 650"),
        ("OnePlus", "OnePlus Nord", 10.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 620"),
        ("OnePlus", "OnePlus 8T", 11.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 650"),
        ("OnePlus", "OnePlus 9 Pro", 11.0, 1440, 3216, 8, 8, "Qualcomm", "Adreno 660"),
        ("OnePlus", "OnePlus Nord 2", 11.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G77"),
        ("OnePlus", "OnePlus 10 Pro", 12.0, 1440, 3216, 8, 8, "Qualcomm", "Adreno 730"),
        ("OnePlus", "OnePlus 10T", 12.0, 1080, 2412, 8, 8, "Qualcomm", "Adreno 730"),
        ("OnePlus", "OnePlus Nord 3", 13.0, 1240, 2772, 8, 8, "MediaTek", "Mali-G710"),
        ("OnePlus", "OnePlus 11", 13.0, 1440, 3216, 8, 8, "Qualcomm", "Adreno 740"),
        ("OnePlus", "OnePlus Open", 13.0, 2268, 2440, 8, 16, "Qualcomm", "Adreno 740"),
        ("OnePlus", "OnePlus 12", 14.0, 1440, 3168, 8, 12, "Qualcomm", "Adreno 750"),
        ("OnePlus", "OnePlus Nord 4", 14.0, 1240, 2772, 8, 12, "Qualcomm", "Adreno 732"),
        # Tecno
        ("Tecno", "Camon 15", 10.0, 720, 1600, 8, 4, "MediaTek", "PowerVR GE8320"),
        ("Tecno", "Pouvoir 4", 10.0, 720, 1640, 4, 3, "MediaTek", "PowerVR GE8300"),
        ("Tecno", "Camon 17 Pro", 11.0, 1080, 2460, 8, 8, "MediaTek", "Mali-G76"),
        ("Tecno", "Phantom X", 11.0, 1080, 2340, 8, 8, "MediaTek", "Mali-G76"),
        ("Tecno", "Spark 8 Pro", 11.0, 1080, 2460, 8, 4, "MediaTek", "Mali-G52"),
        ("Tecno", "Camon 18 Premier", 11.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G57"),
        ("Tecno", "Pova 3", 12.0, 1080, 2460, 8, 4, "MediaTek", "Mali-G52"),
        ("Tecno", "Camon 19 Pro", 12.0, 1080, 2460, 8, 8, "MediaTek", "Mali-G57"),
        ("Tecno", "Phantom X2 Pro", 12.0, 1080, 2400, 8, 12, "MediaTek", "Mali-G710"),
        ("Tecno", "Spark 10 Pro", 13.0, 1080, 2460, 8, 8, "MediaTek", "Mali-G52"),
        ("Tecno", "Camon 20 Premier", 13.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G710"),
        ("Tecno", "Phantom V Fold", 13.0, 2000, 2296, 8, 12, "MediaTek", "Mali-G710"),
        ("Tecno", "Pova 5 Pro", 13.0, 1080, 2460, 8, 8, "MediaTek", "Mali-G57"),
        ("Tecno", "Camon 30 Premier", 14.0, 1264, 2780, 8, 12, "MediaTek", "Mali-G610"),
        ("Tecno", "Phantom V Flip", 13.0, 1080, 2640, 8, 8, "MediaTek", "Mali-G77"),
        ("Tecno", "Spark 20 Pro", 14.0, 1080, 2460, 8, 8, "MediaTek", "Mali-G57"),
        # Infinix
        ("Infinix", "Note 7", 10.0, 720, 1640, 8, 4, "MediaTek", "Mali-G52"),
        ("Infinix", "Zero 8", 10.0, 1080, 2460, 8, 8, "MediaTek", "Mali-G76"),
        ("Infinix", "Note 10 Pro", 11.0, 1080, 2460, 8, 8, "MediaTek", "Mali-G76"),
        ("Infinix", "Zero X Pro", 11.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G76"),
        ("Infinix", "Hot 11", 11.0, 1080, 2408, 8, 4, "MediaTek", "Mali-G52"),
        ("Infinix", "Note 12 VIP", 12.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G57"),
        ("Infinix", "Zero Ultra", 12.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G68"),
        ("Infinix", "Hot 20", 12.0, 1080, 2460, 8, 4, "MediaTek", "Mali-G52"),
        ("Infinix", "Note 30 VIP", 13.0, 1080, 2400, 8, 12, "MediaTek", "Mali-G77"),
        ("Infinix", "Zero 30 5G", 13.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G77"),
        ("Infinix", "GT 10 Pro", 13.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G77"),
        ("Infinix", "Hot 40 Pro", 13.0, 1080, 2460, 8, 8, "MediaTek", "Mali-G57"),
        ("Infinix", "Note 40 Pro+", 14.0, 1080, 2436, 8, 12, "MediaTek", "Mali-G68"),
        ("Infinix", "GT 20 Pro", 14.0, 1080, 2436, 8, 12, "MediaTek", "Mali-G610"),
        ("Infinix", "Zero 40", 14.0, 1080, 2436, 8, 12, "MediaTek", "Mali-G610"),
        # Honor
        ("Honor", "Honor 30 Pro", 10.0, 1080, 2340, 8, 8, "Huawei", "Mali-G76"),
        ("Honor", "Honor 50", 11.0, 1080, 2340, 8, 8, "Qualcomm", "Adreno 642L"),
        ("Honor", "Honor 60 Pro", 11.0, 1200, 2652, 8, 8, "Qualcomm", "Adreno 642L"),
        ("Honor", "Magic 4 Pro", 12.0, 1312, 2848, 8, 8, "Qualcomm", "Adreno 730"),
        ("Honor", "Honor 70", 12.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 642L"),
        ("Honor", "Honor 80 Pro", 12.0, 1224, 2700, 8, 8, "Qualcomm", "Adreno 730"),
        ("Honor", "Magic 5 Pro", 13.0, 1312, 2848, 8, 12, "Qualcomm", "Adreno 740"),
        ("Honor", "Honor 90", 13.0, 1200, 2664, 8, 12, "Qualcomm", "Adreno 644"),
        ("Honor", "Magic V2", 13.0, 2156, 2344, 8, 16, "Qualcomm", "Adreno 740"),
        ("Honor", "Honor 100 Pro", 13.0, 1224, 2700, 8, 12, "Qualcomm", "Adreno 730"),
        ("Honor", "Magic 6 Pro", 14.0, 1280, 2800, 8, 12, "Qualcomm", "Adreno 750"),
        ("Honor", "Honor 200 Pro", 14.0, 1224, 2700, 8, 12, "Qualcomm", "Adreno 750"),
        ("Honor", "Magic V3", 14.0, 2156, 2344, 8, 12, "Qualcomm", "Adreno 750"),
        # Motorola
        ("Motorola", "Razr (2019)", 9.0, 876, 2142, 8, 6, "Qualcomm", "Adreno 616"),
        ("Motorola", "Edge+ (2020)", 10.0, 1080, 2340, 8, 12, "Qualcomm", "Adreno 650"),
        ("Motorola", "Moto G100", 11.0, 1080, 2520, 8, 8, "Qualcomm", "Adreno 650"),
        ("Motorola", "Edge 20 Pro", 11.0, 1080, 2400, 8, 12, "Qualcomm", "Adreno 650"),
        ("Motorola", "Edge 30 Pro", 12.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 730"),
        ("Motorola", "Razr 2022", 12.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 730"),
        ("Motorola", "Edge 40 Pro", 13.0, 1080, 2400, 8, 12, "Qualcomm", "Adreno 740"),
        ("Motorola", "Razr 40 Ultra", 13.0, 1080, 2640, 8, 8, "Qualcomm", "Adreno 740"),
        ("Motorola", "Moto G84", 13.0, 1080, 2400, 8, 12, "Qualcomm", "Adreno 619"),
        ("Motorola", "Edge 50 Pro", 14.0, 1220, 2712, 8, 12, "Qualcomm", "Adreno 720"),
        ("Motorola", "Razr 50 Ultra", 14.0, 1080, 2640, 8, 12, "Qualcomm", "Adreno 740"),
        ("Motorola", "ThinkPhone", 13.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 730"),
        ("Motorola", "Moto G Stylus 5G (2024)", 14.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 619"),
        ("Motorola", "Moto G Power 5G (2024)", 14.0, 1080, 2400, 8, 8, "MediaTek", "Mali-G57"),
        # Asus
        ("Asus", "Zenfone 6", 9.0, 1080, 2340, 8, 6, "Qualcomm", "Adreno 640"),
        ("Asus", "ROG Phone II", 9.0, 1080, 2340, 8, 8, "Qualcomm", "Adreno 640"),
        ("Asus", "Zenfone 7 Pro", 10.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 650"),
        ("Asus", "ROG Phone 3", 10.0, 1080, 2340, 8, 12, "Qualcomm", "Adreno 650"),
        ("Asus", "Zenfone 8", 11.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 660"),
        ("Asus", "ROG Phone 5", 11.0, 1080, 2448, 8, 8, "Qualcomm", "Adreno 660"),
        ("Asus", "Zenfone 9", 12.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 730"),
        ("Asus", "ROG Phone 6", 12.0, 1080, 2448, 8, 12, "Qualcomm", "Adreno 730"),
        ("Asus", "Zenfone 10", 13.0, 1080, 2400, 8, 8, "Qualcomm", "Adreno 740"),
        ("Asus", "ROG Phone 7", 13.0, 1080, 2448, 8, 12, "Qualcomm", "Adreno 740"),
        ("Asus", "Zenfone 11 Ultra", 14.0, 1080, 2400, 8, 12, "Qualcomm", "Adreno 750"),
        ("Asus", "ROG Phone 8 Pro", 14.0, 1080, 2400, 8, 16, "Qualcomm", "Adreno 750"),
        ("Asus", "ROG Phone 8", 14.0, 1080, 2400, 8, 12, "Qualcomm", "Adreno 750"),
        # Sony
        ("Sony", "Xperia 1", 9.0, 1644, 3840, 8, 6, "Qualcomm", "Adreno 640"),
        ("Sony", "Xperia 5", 9.0, 1080, 2520, 8, 6, "Qualcomm", "Adreno 640"),
        ("Sony", "Xperia 1 II", 10.0, 1644, 3840, 8, 8, "Qualcomm", "Adreno 650"),
        ("Sony", "Xperia 5 II", 10.0, 1080, 2520, 8, 8, "Qualcomm", "Adreno 650"),
        ("Sony", "Xperia 10 II", 10.0, 1080, 2520, 8, 4, "Qualcomm", "Adreno 610"),
        ("Sony", "Xperia 1 III", 11.0, 1644, 3840, 8, 12, "Qualcomm", "Adreno 660"),
        ("Sony", "Xperia 5 III", 11.0, 1080, 2520, 8, 8, "Qualcomm", "Adreno 660"),
        ("Sony", "Xperia 10 III", 11.0, 1080, 2520, 8, 6, "Qualcomm", "Adreno 619"),
        ("Sony", "Xperia PRO-I", 11.0, 1644, 3840, 8, 12, "Qualcomm", "Adreno 660"),
        ("Sony", "Xperia 1 IV", 12.0, 1644, 3840, 8, 12, "Qualcomm", "Adreno 730"),
        ("Sony", "Xperia 5 IV", 12.0, 1080, 2520, 8, 8, "Qualcomm", "Adreno 730"),
        ("Sony", "Xperia 10 IV", 12.0, 1080, 2520, 8, 6, "Qualcomm", "Adreno 619"),
        ("Sony", "Xperia 1 V", 13.0, 1644, 3840, 8, 12, "Qualcomm", "Adreno 740"),
        ("Sony", "Xperia 5 V", 13.0, 1080, 2520, 8, 8, "Qualcomm", "Adreno 740"),
        ("Sony", "Xperia 10 V", 13.0, 1080, 2520, 8, 6, "Qualcomm", "Adreno 619"),
        ("Sony", "Xperia 1 VI", 14.0, 1080, 2340, 8, 12, "Qualcomm", "Adreno 750"),
        ("Sony", "Xperia 5 VI", 14.0, 1080, 2340, 8, 12, "Qualcomm", "Adreno 750"),
        ("Sony", "Xperia 1 VII", 15.0, 1080, 2340, 8, 16, "Qualcomm", "Adreno 830"),
    ]

    android_final = []
    for brand, model, launch_os, w, h, cpu, ram, vendor, renderer in android_raw_data:
        # Avoid redundant brand if already in model name (e.g. Xiaomi Xiaomi 12 -> Xiaomi 12)
        if model.startswith(brand):
            full_name = model
        else:
            full_name = f"{brand} {model}"
        cams = get_cams(brand, model)
        android_final.append((brand, full_name, str(launch_os), w, h, cpu, ram, 2, 2, cams, vendor, renderer))

    # Shuffle to mix brands
    random.shuffle(android_final)
    return android_final, ios_final

ANDROID_DEVICES, IOS_DEVICES = generate_database()
__all__ = ["ANDROID_DEVICES", "IOS_DEVICES"]
