# sendkey_utils.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import time
import random

def _get_selenium_driver():
    """SeleniumLibrary'den aktif WebDriver örneğini alır"""
    try:
        selenium_lib = BuiltIn().get_library_instance('SeleniumLibrary')
        return selenium_lib.driver
    except Exception as e:
        print(f"WebDriver alınamadı: {e}")
        return None

@keyword("Highlight With Circle")
def highlight_with_circle(locator, color="yellow", duration=1, radius=10):
    """Elementin merkezine dairesel işaret koy"""
    driver = _get_selenium_driver()
    if not driver:
        return

    try:
        # Locator string ise elementi bul
        if isinstance(locator, str):
            if locator.startswith("xpath="):
                locator = locator.replace("xpath=", "", 1)
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.XPATH, locator)))
        else:
            element = locator

        # Elementin konumunu ve boyutunu al
        location = element.location
        size = element.size

        # Merkez noktasını hesapla
        center_x = location['x'] + size['width'] / 2
        center_y = location['y'] + size['height'] / 2

        # Dairesel işaret ekle (JavaScript ile)
        script = f"""
            // Önce eski işaretleri temizle
            var oldMarker = document.getElementById('robot-marker');
            if(oldMarker) oldMarker.remove();

            // Yeni işaret oluştur
            var marker = document.createElement('div');
            marker.id = 'robot-marker';
            marker.style.position = 'absolute';
            marker.style.left = '{center_x - radius}px';
            marker.style.top = '{center_y - radius}px';
            marker.style.width = '{radius * 2}px';
            marker.style.height = '{radius * 2}px';
            marker.style.borderRadius = '50%';
            marker.style.border = '3px solid {color}';
            marker.style.backgroundColor = 'rgba(255, 255, 0, 0.2)';
            marker.style.zIndex = '9999';
            marker.style.pointerEvents = 'none';
            marker.style.boxShadow = '0 0 15px rgba(0,0,0,0.3)';

            // Animasyon ekle
            marker.style.animation = 'pulse 0.8s ease-in-out';
            var style = document.createElement('style');
            style.innerHTML = `
                @keyframes pulse {{
                    0% {{ transform: scale(1); opacity: 0.8; }}
                    50% {{ transform: scale(1.2); opacity: 1; }}
                    100% {{ transform: scale(1); opacity: 0.8; }}
                }}
            `;
            document.head.appendChild(style);

            document.body.appendChild(marker);

            // Belirtilen süre sonra işareti kaldır
            setTimeout(function() {{
                var marker = document.getElementById('robot-marker');
                if(marker) marker.remove();
            }}, {duration * 1000});
        """
        driver.execute_script(script)
        time.sleep(duration)
    except Exception as e:
        print(f"[highlight_with_circle] ⚠ İşaret eklenirken hata: {str(e)}")


@keyword("Smart Send Keys")
def send_keys_smartly(locator, text, clear_first=True, press_enter=False,
                      human_like=False, delay=0.1, highlight_color="yellow",
                      timeout=10, show_circle=True):
    """
    GELİŞMİŞ YAZMA FONKSİYONU - Robot Framework keyword'ü

    Args:
        locator: Element locator'ı (XPATH string)
        text: Yazılacak metin
        clear_first: Önce temizleme (default: True)
        press_enter: Enter tuşuna bas (default: False)
        human_like: İnsan gibi yavaş yaz (default: False)
        delay: Karakter arası gecikme (default: 0.1sn)
        highlight_color: Vurgu rengi (default: "yellow")
        timeout: Bekleme süresi (default: 10sn)
        show_circle: Merkeze daire işareti koy (default: True)

    Returns:
        bool: İşlem başarılı mı?
    """
    driver = _get_selenium_driver()
    if not driver:
        print("[Smart Send Keys] ❌ WebDriver bulunamadı!")
        return False

    # Locator temizleme (xpath= öneki varsa kaldır)
    clean_locator = locator
    if locator.startswith("xpath="):
        clean_locator = locator.replace("xpath=", "", 1)

    print(f"\n{'=' * 70}")
    print(f"[Smart Send Keys] 🚀 Yazma işlemi başlıyor...")
    print(f"[Smart Send Keys]    ├─ Metin: '{text}'")
    print(f"[Smart Send Keys]    ├─ Locator: {locator}")
    print(f"[Smart Send Keys]    ├─ İnsan gibi: {human_like}")
    print(f"[Smart Send Keys]    ├─ Enter: {press_enter}")
    print(f"[Smart Send Keys]    └─ Daire işareti: {'Evet' if show_circle else 'Hayır'}")
    print(f"{'=' * 70}")

    try:
        # 1. Elementi bul
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.XPATH, clean_locator)))

        # Element bilgilerini al
        tag = element.tag_name
        element_type = element.get_attribute('type')
        is_displayed = element.is_displayed()
        is_enabled = element.is_enabled()
        current_value = element.get_attribute('value') or '[empty]'

        print(f"[Smart Send Keys] 🔍 Element bilgileri:")
        print(f"[Smart Send Keys]    ├─ Tag: <{tag}>")
        print(f"[Smart Send Keys]    ├─ Type: {element_type}")
        print(f"[Smart Send Keys]    ├─ Görünür: {is_displayed}")
        print(f"[Smart Send Keys]    ├─ Etkin: {is_enabled}")
        print(f"[Smart Send Keys]    └─ Mevcut değer: '{current_value[:30]}...'")

        # Elementi vurgula ve daire işareti koy
        if show_circle:
            highlight_with_circle(element, highlight_color, 0.8)
        else:
            # Eski highlight fonksiyonu
            original_style = element.get_attribute('style')
            driver.execute_script(
                f"arguments[0].setAttribute('style', arguments[1]);",
                element,
                f"border: 3px solid {highlight_color}; background: #ffff99;"
            )
            time.sleep(0.3)
            driver.execute_script(
                f"arguments[0].setAttribute('style', arguments[1]);",
                element,
                original_style
            )

        # ============= YAZMA YÖNTEMLERİ =============

        # YÖNTEM 1: Normal send_keys
        try:
            if clear_first:
                element.clear()
                time.sleep(0.2)

            if human_like:
                # İnsan gibi yazma
                for char in text:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
            else:
                element.send_keys(text)

            if press_enter:
                element.send_keys(Keys.RETURN)
                print(f"[Smart Send Keys] ✅ Enter tuşuna basıldı")

            print(f"[Smart Send Keys] ✅ Yöntem 1 (Normal send_keys) BAŞARILI")
            return True

        except ElementNotInteractableException:
            print(f"[Smart Send Keys] ⚠ Yöntem 1 başarısız - Element etkileşime kapalı")
        except Exception as e:
            print(f"[Smart Send Keys] ⚠ Yöntem 1 başarısız - {str(e)[:50]}...")

        # YÖNTEM 2: JavaScript ile yazma
        try:
            if clear_first:
                driver.execute_script("arguments[0].value = '';", element)

            driver.execute_script(f"arguments[0].value = '{text}';", element)

            # Input event'ini tetikle
            driver.execute_script("""
                var event = new Event('input', { bubbles: true });
                arguments[0].dispatchEvent(event);
            """, element)

            if press_enter:
                driver.execute_script("""
                    var event = new KeyboardEvent('keydown', {
                        key: 'Enter',
                        code: 'Enter',
                        keyCode: 13,
                        which: 13,
                        bubbles: true
                    });
                    arguments[0].dispatchEvent(event);
                """, element)

            print(f"[Smart Send Keys] ✅ Yöntem 2 (JavaScript) BAŞARILI")
            return True
        except Exception as e:
            print(f"[Smart Send Keys] ⚠ Yöntem 2 başarısız - {str(e)[:50]}...")

        # YÖNTEM 3: ActionChains ile
        try:
            actions = ActionChains(driver)
            actions.move_to_element(element).click()

            if clear_first:
                actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
                actions.send_keys(Keys.DELETE)

            if human_like:
                for char in text:
                    actions.send_keys(char)
                    actions.pause(random.uniform(0.05, 0.15))
            else:
                actions.send_keys(text)

            if press_enter:
                actions.send_keys(Keys.RETURN)

            actions.perform()
            print(f"[Smart Send Keys] ✅ Yöntem 3 (ActionChains) BAŞARILI")
            return True
        except Exception as e:
            print(f"[Smart Send Keys] ⚠ Yöntem 3 başarısız - {str(e)[:50]}...")

        print(f"[Smart Send Keys] ❌ TÜM YÖNTEMLER BAŞARISIZ!")
        return False

    except TimeoutException:
        print(f"[Smart Send Keys] ❌ Element bulunamadı: {locator}")
        return False