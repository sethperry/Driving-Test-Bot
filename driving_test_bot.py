import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

# Telegram Bot API details
BOT_TOKEN = "7917562169:AAETjFsGYBl1-m0AquzjqUfrQ4z9wibgUeA"
CHAT_ID = "7256447006"

def send_telegram_notification(message):
    """Send a notification message via Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Telegram notification sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram notification: {e}")

def find_and_book_slot():
    driver = webdriver.Chrome()
    try:
        # Step 1: Open the initial webpage
        driver.get("https://www.service.transport.qld.gov.au/SBSExternal/public/WelcomeDrivingTest.xhtml?dswid=-5059")
        
        # Step 2: Click the "Continue" button on the first page
        wait = WebDriverWait(driver, 10)
        continue_button = wait.until(
            EC.visibility_of_element_located((By.ID, "j_id_60:aboutThisServiceForm:continueButton"))
        )
        continue_button.click()
        print("Clicked the 'Continue' button.")

        # Step 3: Accept Terms and Conditions
        wait.until(EC.url_contains("TermsAndConditions"))
        accept_button = wait.until(
            EC.visibility_of_element_located((By.ID, "termsAndConditions:TermsAndConditionsForm:acceptButton"))
        )
        accept_button.click()
        print("Accepted terms and conditions.")

        # Step 4: Fill in license details and proceed
        wait.until(EC.url_contains("CleanBookingDE"))
        license_number_field = wait.until(
            EC.presence_of_element_located((By.ID, "CleanBookingDEForm:dlNumber"))
        )
        license_number_field.send_keys("134361060")
        contact_name_field = driver.find_element(By.ID, "CleanBookingDEForm:contactName")
        contact_name_field.send_keys("Seth Perry")
        contact_phone_field = driver.find_element(By.ID, "CleanBookingDEForm:contactPhone")
        contact_phone_field.send_keys("0477041755")

        dropdown_trigger = driver.find_element(By.CLASS_NAME, "ui-selectonemenu-trigger")
        dropdown_trigger.click()
        desired_option = wait.until(
            EC.element_to_be_clickable((By.ID, "CleanBookingDEForm:productType_1"))
        )
        desired_option.click()

        continue_button = driver.find_element(By.ID, "CleanBookingDEForm:actionFieldList:confirmButtonField:confirmButton")
        continue_button.click()
        print("Clicked 'Continue' on license details page.")

        # Step 5: Confirm license details
        wait.until(EC.url_contains("LicenceDetailsConfirmation"))
        confirmation_continue_button = wait.until(
            EC.element_to_be_clickable((By.ID, "BookingConfirmationForm:actionFieldList:confirmButtonField:confirmButton"))
        )
        confirmation_continue_button.click()
        print("Confirmed license details.")

        # Step 6: Select location
        wait.until(EC.url_contains("LocationSelection"))
        location_dropdown_trigger = driver.find_element(By.CLASS_NAME, "ui-selectonemenu-trigger")
        location_dropdown_trigger.click()
        desired_location_option = wait.until(
            EC.element_to_be_clickable((By.ID, "BookingSearchForm:region_15"))  # SEQ IPSWICH
        )
        desired_location_option.click()
        location_continue_button = wait.until(
            EC.element_to_be_clickable((By.ID, "BookingSearchForm:actionFieldList:confirmButtonField:confirmButton"))
        )
        location_continue_button.click()
        print("Clicked 'Continue' on location selection page.")

        # Step 7: Check available slots
        wait.until(EC.url_contains("SlotSelection"))
        slot_labels = driver.find_elements(By.TAG_NAME, "label")
        today = datetime.today()
        seven_days_from_now = today + timedelta(days=7)

        for label in slot_labels:
            slot_date_text = label.text.strip()
            try:
                slot_date = datetime.strptime(slot_date_text, "%A, %d %B %Y %I:%M %p")
                if today <= slot_date <= seven_days_from_now:
                    label_for = label.get_attribute("for")
                    radio_button = driver.find_element(By.ID, label_for)
                    radio_button.click()
                    print(f"Selected slot: {slot_date_text}")

                    slot_continue_button = driver.find_element(
                        By.ID, "slotSelectionForm:actionFieldList:confirmButtonField:confirmButton"
                    )
                    slot_continue_button.click()
                    print("Booking confirmed. Proceeding to final confirmation.")

                    # Step 8: Final confirmation page
                    wait.until(EC.url_contains("NewBookingConfirmation"))
                    final_confirm_button = wait.until(
                        EC.element_to_be_clickable((By.ID, "BookingConfirmationForm:actionFieldList:confirmButtonField:confirmButton"))
                    )
                    final_confirm_button.click()
                    print("Booking successfully finalized! Proceeding to payment.")

                    # Step 9: Payment email entry
                    wait.until(EC.url_contains("ShoppingBasket"))
                    email_field = wait.until(
                        EC.presence_of_element_located((By.ID, "paymentOptionSelectionForm:paymentOptions:emailAddressField:emailAddress"))
                    )
                    email_field.send_keys("sethperry000@gmail.com")
                    print("Entered email address.")

                    payment_continue_button = driver.find_element(
                        By.ID, "paymentOptionSelectionForm:buttonFieldList:payNowField:payNowButton"
                    )
                    payment_continue_button.click()
                    print("Payment process initiated. Proceeding to card entry.")

                    # Step 10: Payment card entry
                    wait.until(EC.url_contains("bpoint"))
                    card_number_field = wait.until(
                        EC.presence_of_element_located((By.ID, "CardNumber"))
                    )
                    card_number_field.send_keys("4934140521101920")
                    expiry_month_field = driver.find_element(By.ID, "ExpiryMonth")
                    expiry_month_field.send_keys("01")
                    expiry_year_field = driver.find_element(By.ID, "ExpiryYear")
                    expiry_year_field.send_keys("27")
                    cvv_field = driver.find_element(By.ID, "CVN")
                    cvv_field.send_keys("232")

                    review_payment_button = driver.find_element(By.ID, "btnReviewPayment")
                    review_payment_button.click()
                    print("Clicked 'Next' on payment page.")

                    # Step 11: Final Pay Button
                    pay_button = wait.until(
                        EC.element_to_be_clickable((By.ID, "btnProcessPayment"))
                    )
                    pay_button.click()
                    print("Payment processed successfully. Booking complete!")

                    send_telegram_notification(f"Driving test slot booked successfully for {slot_date_text}. Payment processed!")
                    return True
            except ValueError:
                continue

        print("No suitable slots found.")
        send_telegram_notification("No suitable driving test slots were found. Retrying later.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        send_telegram_notification(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    if find_and_book_slot():
        print("Test booked successfully.")
    else:
        print("No suitable slots found.")
