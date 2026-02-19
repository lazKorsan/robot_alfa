# click_utils.py
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import time

def _get_selenium_driver():
    """SeleniumLibrary'den aktif WebDriver örneğini alır"""
    try:
        selenium_lib = BuiltIn().get_library_instance('SeleniumLibrary')
        return selenium_lib.driver
    except Exception as e:
        logger.error(f"WebDriver alınamadı: {e}")
        return None

@keyword("Highlight With Circle Click")
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
            marker.style.backgroundColor = 'rgba(255, 255, 0, 0.3)';
            marker.style.zIndex = '9999';
            marker.style.pointerEvents = 'none';
            marker.style.boxShadow = '0 0 10px rgba(0,0,0,0.5)';

            // Animasyon ekle
            marker.style.animation = 'pulse 0.5s ease-in-out';
            var style = document.createElement('style');
            style.innerHTML = `
                @keyframes pulse {{
                    0% {{ transform: scale(1); opacity: 1; }}
                    50% {{ transform: scale(1.3); opacity: 0.7; }}
                    100% {{ transform: scale(1); opacity: 1; }}
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
        logger.warn(f"[highlight_with_circle] ⚠ İşaret eklenirken hata: {str(e)}")


@keyword("Smart Click Element")
def smart_click_element(xpath, color="yellow", timeout=10, show_circle=True):
    """
    İnatçı butonlar için gelişmiş tıklama fonksiyonu - Robot Framework keyword'ü

    Args:
        xpath: Butonun XPATH'i
        color: Vurgu rengi (default: yellow)
        timeout: Bekleme süresi (default: 10)
        show_circle: Merkeze daire işareti koy (default: True)

    Returns:
        bool: Tıklama başarılı mı?
    """
    driver = _get_selenium_driver()
    if not driver:
        logger.error("[Smart Click Element] ❌ WebDriver bulunamadı!")
        return False

    # Locator temizleme (xpath= öneki varsa kaldır)
    clean_locator = xpath
    if xpath.startswith("xpath="):
        clean_locator = xpath.replace("xpath=", "", 1)

    logger.info(f"\n{'=' * 60}")
    logger.info(f"[Smart Click Element] 🚀 Buton tıklama denemesi başlıyor...")
    logger.info(f"[Smart Click Element]    ├─ XPATH: {xpath}")
    logger.info(f"[Smart Click Element]    ├─ Renk: {color}")
    logger.info(f"[Smart Click Element]    ├─ Timeout: {timeout}sn")
    logger.info(f"[Smart Click Element]    └─ Daire işareti: {'Evet' if show_circle else 'Hayır'}")
    logger.info(f"{'=' * 60}")

    try:
        # 1. Elementi bul ve tıklanabilir olana kadar bekle
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, clean_locator)))

        # Element bilgilerini al
        visible = element.is_displayed()
        enabled = element.is_enabled()
        text = element.text.strip() or element.get_attribute('value') or element.get_attribute('innerText') or 'NoText'
        tag = element.tag_name

        logger.info(f"[Smart Click Element] 🔍 Buton bilgileri:")
        logger.info(f"[Smart Click Element]    ├─ Tag: <{tag}>")
        logger.info(f"[Smart Click Element]    ├─ Text: '{text}'")
        logger.info(f"[Smart Click Element]    ├─ Görünür: {visible}")
        logger.info(f"[Smart Click Element]    └─ Tıklanabilir: {enabled}")

        # Elementi vurgula ve daire işareti koy
        if show_circle:
            highlight_with_circle(element, color, 1)
        else:
            # Eski highlight fonksiyonu
            original_style = element.get_attribute('style')
            driver.execute_script(
                f"arguments[0].setAttribute('style', arguments[1]);",
                element,
                f"border: 3px solid {color}; background: #ffff99;"
            )
            time.sleep(0.5)
            driver.execute_script(
                f"arguments[0].setAttribute('style', arguments[1]);",
                element,
                original_style
            )

        # ============= TIKLAMA YÖNTEMLERİ =============

        # YÖNTEM 1: Normal click
        try:
            element.click()
            logger.info(f"[Smart Click Element] ✅ Yöntem 1 (Normal click) BAŞARILI: '{text}'")
            return True

        except ElementClickInterceptedException:
            logger.warn(f"[Smart Click Element] ⚠ Yöntem 1 başarısız - Element başka element tarafından engelleniyor")
        except Exception as e:
            logger.warn(f"[Smart Click Element] ⚠ Yöntem 1 başarısız - {str(e)[:50]}...")

        # YÖNTEM 2: JavaScript click
        try:
            driver.execute_script("arguments[0].click();", element)
            logger.info(f"[Smart Click Element] ✅ Yöntem 2 (JavaScript click) BAŞARILI: '{text}'")
            return True
        except Exception as e:
            logger.warn(f"[Smart Click Element] ⚠ Yöntem 2 başarısız - {str(e)[:50]}...")

        # YÖNTEM 3: ActionChains
        try:
            actions = ActionChains(driver)
            actions.move_to_element(element).click().perform()
            logger.info(f"[Smart Click Element] ✅ Yöntem 3 (ActionChains) BAŞARILI: '{text}'")
            return True
        except Exception as e:
            logger.warn(f"[Smart Click Element] ⚠ Yöntem 3 başarısız - {str(e)[:50]}...")

        # YÖNTEM 4: Scroll + click
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.5)
            element.click()
            logger.info(f"[Smart Click Element] ✅ Yöntem 4 (Scroll + click) BAŞARILI: '{text}'")
            return True
        except Exception as e:
            logger.warn(f"[Smart Click Element] ⚠ Yöntem 4 başarısız - {str(e)[:50]}...")

        logger.error(f"[Smart Click Element] ❌ TÜM YÖNTEMLER BAŞARISIZ! Butona tıklanamadı: '{text}'")
        return False

    except TimeoutException:
        logger.error(f"[Smart Click Element] ❌ Buton bulunamadı veya tıklanabilir değil: {xpath}")
        return False

    except Exception as e:
        logger.error(f"[Smart Click Element] ❌ Beklenmeyen hata: {str(e)}")
        return False


@keyword("Smart Click Element By Text")
def smart_click_element_by_text(text, tag="button", color="purple", timeout=10, show_circle=True):
    """Buton metnine göre tıkla"""
    xpath = f"//{tag}[contains(text(), '{text}')]"
    logger.info(f"[Smart Click Element] 🔍 Metin ile buton aranıyor: '{text}'")
    return smart_click_element(xpath, color, timeout, show_circle)


@keyword("Smart Click Element By CSS")
def smart_click_element_by_css(css_selector, color="blue", timeout=10, show_circle=True):
    """CSS Selector ile tıkla"""
    driver = _get_selenium_driver()
    if not driver:
        return False

    logger.info(f"[Smart Click Element] 🔍 CSS Selector ile buton aranıyor: {css_selector}")

    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )

        if show_circle:
            highlight_with_circle(element, color, 1)

        element.click()
        logger.info(f"[Smart Click Element] ✅ CSS Selector tıklama başarılı!")
        return True
    except:
        # CSS selector'ı XPath'e dönüştürmek her zaman güvenilir değildir, bu yüzden basit bir ID varsayımı yapalım
        return smart_click_element(f"//*[@id='{css_selector}']", color, timeout, show_circle)


@keyword("Verify Element Text And Highlight")
def verify_element_text_and_highlight(locator, expected_text, color="lime", timeout=10, duration=2):
    """
    Elementin metnini doğrular ve elementi dairesel olarak işaretler.

    Args:
        locator: Elementin locator'ı (örn: xpath=//a)
        expected_text: Beklenen metin
        color: Vurgu rengi (default: lime)
        timeout: Elementi bulmak için bekleme süresi (default: 10)
        duration: Vurgunun ekranda kalma süresi (default: 2)

    Raises:
        AssertionError: Element bulunamazsa veya metin eşleşmezse.
    """
    driver = _get_selenium_driver()
    if not driver:
        raise AssertionError("WebDriver alınamadı!")

    clean_locator = locator
    if locator.startswith("xpath="):
        clean_locator = locator.replace("xpath=", "", 1)

    logger.info(f"Metin doğrulaması ve vurgulama başlıyor: {locator}")
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.XPATH, clean_locator)))

        logger.info("Element bulundu, vurgulanıyor...")
        highlight_with_circle(element, color, duration=duration)

        actual_text = element.text.strip()
        logger.info(f"Gerçekleşen metin: '{actual_text}', Beklenen metin: '{expected_text}'")

        if actual_text != expected_text:
            raise AssertionError(f"METİN DOĞRULAMASI BAŞARISIZ! Beklenen: '{expected_text}', Gelen: '{actual_text}'")

        logger.info("✅ Metin doğrulaması BAŞARILI!")

    except TimeoutException:
        logger.error(f"DOĞRULAMA HATASI: Element {timeout} saniye içinde bulunamadı: {locator}")
        raise AssertionError(f"Element bulunamadı: {locator}")
