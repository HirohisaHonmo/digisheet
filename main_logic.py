import configparser
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = None


def read_config(file_path):
    """configファイルを読み込みます。"""
    config = configparser.ConfigParser()
    config.read(file_path, encoding="utf-8")

    return config


def init_chrome_driver():
    """ChromeDriver の初期設定を行います。"""
    global driver

    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)


def log_in_to_digisheet(URL_DIGISHEET, COMPANY_CODE, STAFF_CODE, PASSWORD):
    """digisheet にログインします。"""
    global driver

    driver.get(URL_DIGISHEET)

    XPATH_COMPANY_CODE = (
        "/html/body/form/center/table/tbody/tr/td/table/tbody/tr[3]/td/input"
    )
    company_code_textbox = driver.find_element(By.XPATH, XPATH_COMPANY_CODE)
    company_code_textbox.send_keys(COMPANY_CODE)

    XPATH_STAFF_ID = (
        "/html/body/form/center/table/tbody/tr/td/table/tbody/tr[4]/td/input"
    )
    staff_id_textbox = driver.find_element(By.XPATH, XPATH_STAFF_ID)
    staff_id_textbox.send_keys(STAFF_CODE)

    XPATH_PASSWORD = (
        "/html/body/form/center/table/tbody/tr/td/table/tbody/tr[5]/td/input"
    )
    password_textbox = driver.find_element(By.XPATH, XPATH_PASSWORD)
    password_textbox.send_keys(PASSWORD)

    XPATH_LOGIN_BUTTON = "/html/body/form/center/table/tbody/tr/td/table/tbody/tr[6]/td/table/tbody/tr/th[1]/input"
    login_button = driver.find_element(By.XPATH, XPATH_LOGIN_BUTTON)
    login_button.click()


def click_work_report():
    """勤務報告に遷移します。"""
    global driver

    NAME_ATTRIBUTE_MENU_FRAME = "menu"
    menu_frame = driver.find_element(By.NAME, NAME_ATTRIBUTE_MENU_FRAME)
    driver.switch_to.frame(menu_frame)

    XPATH_WORK_TIME_REPORT = "/html/body/form/div[4]/table/tbody/tr[7]/td/a"
    work_time_report_link = driver.find_element(By.XPATH, XPATH_WORK_TIME_REPORT)
    work_time_report_link.click()

    driver.switch_to.default_content()


def is_special_leave_or_paid_vacation(row_num_of_target_day):
    """有給休暇や特別休暇などを届け出ているか確認します。 A勤務でも空白でもなければ、何らかの申請をしていると判断します。"""
    global driver

    xpath_application_status = (
        "/html/body/form/table/tbody/tr[7]/td/table/tbody/tr["
        + row_num_of_target_day
        + "]/td[8]/font"
    )
    application_status_table_data = driver.find_element(
        By.XPATH, xpath_application_status
    )
    application_status_text = application_status_table_data.text

    WORK_PATTERN_A = "Ａ勤務"
    WORK_PATTERN_BLANK = " "
    if (
        application_status_text == WORK_PATTERN_A
        or application_status_text == WORK_PATTERN_BLANK
    ):
        return False
    else:
        return True


def is_registered(row_num_of_target_day):
    """勤務データが登録済みか確認します。"""
    global driver

    xpath_working_hour_table_data = (
        "/html/body/form/table/tbody/tr[7]/td/table/tbody/tr["
        + row_num_of_target_day
        + "]/td[9]/font"
    )
    working_hour_table_data = driver.find_element(
        By.XPATH, xpath_working_hour_table_data
    )
    registered_working_hour = working_hour_table_data.text

    # 空白に見える勤務時間列の要素の文字数を確認したところ、3 が返ってきた。0ではなかった。
    # おそらく、「&nbsp;」とその前後の空白を計測しているのではないかと考えられる。
    # 従って、4 以上の場合は勤務情報が登録されていると判断します。
    NUM_BLANK_CHARS = 3
    if len(registered_working_hour) > NUM_BLANK_CHARS:
        return True
    else:
        return False


def is_work_day(row_num_of_target_day):
    """行の背景色が白い場合は営業日と判断します。"""
    global driver

    xpath_table_row = (
        "/html/body/form/table/tbody/tr[7]/td/table/tbody/tr["
        + row_num_of_target_day
        + "]"
    )
    table_row = driver.find_element(By.XPATH, xpath_table_row)
    bgcolor_of_table_row = table_row.value_of_css_property("background-color")

    WHITE = "rgba(255, 255, 255, 1)"
    if bgcolor_of_table_row == WHITE:
        return True
    else:
        return False


def click_link_to_target_day(row_num_of_target_day):
    """営業日のリンクをクリックします。"""
    xpath_anchor_tag = (
        "/html/body/form/table/tbody/tr[7]/td/table/tbody/tr["
        + row_num_of_target_day
        + "]/td[3]/a"
    )
    link_to_target_day = driver.find_element(By.XPATH, xpath_anchor_tag)
    link_to_target_day.click()


def apply_for_telecommuting():
    """在宅勤務の設定を行います。"""

    XPATH_TELECOMMUTING = "//*[@id='StaffWorkSheet']/table/tbody/tr[3]/td/table/tbody/tr[5]/td/table/tbody/tr/td/select"
    telecommuting_drop_down = Select(driver.find_element(By.XPATH, XPATH_TELECOMMUTING))
    TELECOMMUTING_VALUE = "0000000600"
    telecommuting_drop_down.select_by_value(TELECOMMUTING_VALUE)


def deregister_work_report():
    """登録した勤務データの削除を行います。（開発用、登録したデータを消すのが面倒だから。）"""
    XPATH_DEREGISTER_WORK_REPORT = '//*[@id="StaffWorkSheet"]/table/tbody/tr[3]/td/table/tbody/tr[8]/td/table/tbody/tr/td/input[2]'
    deregister_work_report_button = driver.find_element(
        By.XPATH, XPATH_DEREGISTER_WORK_REPORT
    )
    deregister_work_report_button.click()


def register_work_report(
    start_hour, start_minute, end_hour, end_minute, telecommuting_flag
):
    """勤務データを登録します。"""
    global driver

    NAME_ATTRIBUTE_START_HOUR_OF_WORK = "HourStart"
    NAME_ATTRIBUTE_START_MINUTE_OF_WORK = "MinuteStart"
    NAME_ATTRIBUTE_END_HOUR_OF_WORK = "HourEnd"
    NAME_ATTRIBUTE_END_MINUTE_OF_WORK = "MinuteEnd"

    start_hour_drop_down = Select(
        driver.find_element(By.NAME, NAME_ATTRIBUTE_START_HOUR_OF_WORK)
    )
    start_minute_drop_down = Select(
        driver.find_element(By.NAME, NAME_ATTRIBUTE_START_MINUTE_OF_WORK)
    )
    end_hour_drop_down = Select(
        driver.find_element(By.NAME, NAME_ATTRIBUTE_END_HOUR_OF_WORK)
    )
    end_minute_drop_down = Select(
        driver.find_element(By.NAME, NAME_ATTRIBUTE_END_MINUTE_OF_WORK)
    )

    start_hour_drop_down.select_by_value(start_hour)
    start_minute_drop_down.select_by_value(start_minute)
    end_hour_drop_down.select_by_value(end_hour)
    end_minute_drop_down.select_by_value(end_minute)

    if telecommuting_flag is True:
        apply_for_telecommuting()

    XPATH_REGISTRATION_BUTTON = '//*[@id="StaffWorkSheet"]/table/tbody/tr[3]/td/table/tbody/tr[8]/td/table/tbody/tr/td/input[1]'
    registration_button = driver.find_element(By.XPATH, XPATH_REGISTRATION_BUTTON)
    registration_button.click()


def register_work_report_if_it_is_target_day(
    start_hour,
    start_minute,
    end_hour,
    end_minute,
    telecommuting_flag,
    registration_start_day,
    registration_end_day,
):
    """設定された処理期間の各営業日に、設定された勤務時間のデータを登録します。"""
    global driver

    NAME_ATTRIBUTE_MENU_FRAME = "main"
    mainFrame = driver.find_element(By.NAME, NAME_ATTRIBUTE_MENU_FRAME)
    driver.switch_to.frame(mainFrame)

    # 勤務実績が未入力の日に、勤務データを登録していきます。
    # 繰り返しの回数は、（処理終了日 - 処理開始日 + 1）で算出する。
    # 開始日と終了日が同じ日だとしても、繰り返しの回数を 1 にするために +1 で調整しています。
    for i in range(int(registration_end_day) - int(registration_start_day) + 1):
        # 一日（ついたち）の行は tr[2] から始まっているので、row_num_of_target_day が最小でも 2 から始まるように + 1 で調整します。
        row_num_of_target_day = str(i + int(registration_start_day) + 1)

        if is_special_leave_or_paid_vacation(row_num_of_target_day):
            continue

        if is_registered(row_num_of_target_day):
            continue

        if is_work_day(row_num_of_target_day):
            click_link_to_target_day(row_num_of_target_day)
            register_work_report(
                start_hour, start_minute, end_hour, end_minute, telecommuting_flag
            )

    driver.switch_to.default_content()

    ALERT = "alert('処理が完了しました。');"
    driver.execute_script(ALERT)


def main(
    staff_code,
    password,
    start_hour,
    start_minute,
    end_hour,
    end_minute,
    telecommuting_flag,
    registration_start_day,
    registration_end_day,
):
    """一連の処理を main メソッドにまとめています。"""
    user_response = messagebox.askokcancel(
        title="実行前確認",
        message="設定した値に基づき勤務データを登録します。\n誤って登録した場合は手動で更新/削除してください。",
        icon="question",
    )

    if user_response is True:
        init_chrome_driver()

        config = read_config("config_local.ini")
        URL_DIGISHEET = config.get("Digisheet", "URL")
        COMPANY_CODE = config.get("Digisheet", "COMPANY_CODE")

        log_in_to_digisheet(URL_DIGISHEET, COMPANY_CODE, staff_code, password)

        click_work_report()

        register_work_report_if_it_is_target_day(
            start_hour,
            start_minute,
            end_hour,
            end_minute,
            telecommuting_flag,
            registration_start_day,
            registration_end_day,
        )
    else:
        return
