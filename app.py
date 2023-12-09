import calendar
import datetime
import locale
import tkinter
import tkinter.ttk as ttk
from tkinter import messagebox

from main_logic import main


def show_tkinter_window():
    """入力画面を表示します。"""
    today = datetime.date.today()
    this_year = today.year
    this_month = today.month
    days_of_month = calendar.monthrange(this_year, this_month)[1]

    tk = tkinter.Tk()
    tk.geometry("300x400")
    tk.title("勤務データ登録するやつ")

    target_year_and_month = "登録処理対象月：" + str(this_year) + "年" + str(this_month) + "月"
    label_target_year_and_month = tkinter.Label(text=target_year_and_month)
    label_target_year_and_month.place(x=20, y=20)

    def is_valid_staff_id(word_before, word_after):
        """適切なスタッフ ID ( 7 ケタ以下 かつ 数字)しか入力させません。"""
        CHARACTOR_UPPER_LIMIT = 7
        CHARACTOR_LOWER_LIMIT = 0

        return (
            (word_after.isdecimal()) and (len(word_after) <= CHARACTOR_UPPER_LIMIT)
        ) or (len(word_after) == CHARACTOR_LOWER_LIMIT)

    label_staff_id = tkinter.Label(text="スタッフID")
    label_staff_id.place(x=20, y=50)
    entry_staff_id = tkinter.Entry(width=15)
    vcmd_is_valid_staff_id = (entry_staff_id.register(is_valid_staff_id), "%s", "%P")
    entry_staff_id.configure(validate="key", vcmd=vcmd_is_valid_staff_id)
    entry_staff_id.place(x=90, y=50)

    label_password = tkinter.Label(text="パスワード")
    label_password.place(x=20, y=80)
    entry_password = tkinter.Entry(show="*", width=15)
    entry_password.place(x=90, y=80)

    label_start_hour = tkinter.Label(text="始業時間")
    label_start_hour.place(x=20, y=130)

    def set_valid_end_hours(event):
        """設定された始業時間（時）により、終業時間（時）のドロップダウンに適切な値を設定する。"""
        end_hours = []
        for i in range(int(drop_down_start_hour.get()), 47):
            end_hours.append(i)

        drop_down_end_hour["values"] = end_hours

    def prohibit_setting_end_time_before_start_time(event):
        """終業時間を始業時間以前に設定することを禁じたい！"""
        start_hour = int(drop_down_start_hour.get())
        end_hour = int(drop_down_end_hour.get())

        if start_hour >= end_hour:
            start_minute = int(drop_down_start_minute.get())
            end_minute = int(drop_down_end_minute.get())

            if start_minute >= end_minute:
                messagebox.showerror("警告", "終業時間が、始業時間以前になっているので直してください。")

    hours = []
    for i in range(0, 47, 1):
        hours.append(i)

    string_var_start_hours = tkinter.StringVar()
    drop_down_start_hour = ttk.Combobox(
        tk, state="readonly", width=3, textvariable=string_var_start_hours
    )
    drop_down_start_hour["values"] = hours
    drop_down_start_hour.place(x=90, y=130)
    drop_down_start_hour.current(9)
    drop_down_start_hour.bind("<<ComboboxSelected>>", set_valid_end_hours)
    drop_down_start_hour.bind(
        "<<ComboboxSelected>>", prohibit_setting_end_time_before_start_time, "+"
    )

    label_colon_for_start_time = tkinter.Label(text=":")
    label_colon_for_start_time.place(x=135, y=130)

    minutes = []
    for i in range(0, 60, 5):
        minutes.append(i)

    drop_down_start_minute = ttk.Combobox(tk, state="readonly", width=3)
    drop_down_start_minute["values"] = minutes
    drop_down_start_minute.place(x=145, y=130)
    # 20分を初期値にしたいので、4を設定している。分のドロップダウンは5分刻みになっている。
    drop_down_start_minute.current(4)
    drop_down_start_minute.bind(
        "<<ComboboxSelected>>", prohibit_setting_end_time_before_start_time
    )

    label_end_hour = tkinter.Label(text="終業時間")
    label_end_hour.place(x=20, y=160)

    def set_appropriate_start_hours(event):
        """設定された終業時間（時）により、始業時間（時）のドロップダウンに適切な値を設定する。"""
        start_hours = []
        for i in range(0, int(drop_down_end_hour.get()) + 1):
            start_hours.append(i)

        drop_down_start_hour["values"] = start_hours

    string_var_end_hours = tkinter.StringVar()
    drop_down_end_hour = ttk.Combobox(
        tk, state="readonly", width=3, textvariable=string_var_end_hours
    )
    drop_down_end_hour["values"] = hours
    drop_down_end_hour.place(x=90, y=160)
    drop_down_end_hour.current(18)
    drop_down_end_hour.bind("<<ComboboxSelected>>", set_appropriate_start_hours)
    drop_down_end_hour.bind(
        "<<ComboboxSelected>>", prohibit_setting_end_time_before_start_time, "+"
    )

    label_colon_for_end_time = tkinter.Label(text=":")
    label_colon_for_end_time.place(x=135, y=160)

    drop_down_end_minute = ttk.Combobox(tk, state="readonly", width=3)
    drop_down_end_minute["values"] = minutes
    drop_down_end_minute.place(x=145, y=160)
    drop_down_end_minute.current(0)
    drop_down_end_minute.bind(
        "<<ComboboxSelected>>", prohibit_setting_end_time_before_start_time
    )

    telecommuting_flag = tkinter.BooleanVar()
    check_box_telecommuting = tkinter.Checkbutton(
        tk, text="在宅勤務", variable=telecommuting_flag
    )
    check_box_telecommuting.place(x=190, y=160)

    label_registration_period = tkinter.Label(text="処理期間")
    label_registration_period.place(x=20, y=200)

    def change_options_for_registration_end_day(event):
        """設定された登録処理開始日により、登録処理終了日のドロップダウンに適切な値を設定する。"""
        registration_end_days = []
        for i in range(int(drop_down_registration_start_day.get()), days_of_month + 1):
            registration_end_days.append(i)

        drop_down_registration_end_day["values"] = registration_end_days

    def get_day_of_week_in_japanese(YEAR, MONTH, DAY):
        """日本語で曜日を取得します。"""
        locale.setlocale(locale.LC_TIME, "")

        day_of_week = datetime.date(YEAR, MONTH, DAY)
        return "(" + day_of_week.strftime("%a") + ")"

    def set_day_of_week_for_registration_start_day(event):
        """選択された日に応じた曜日を、処理開始日に設定する。"""
        selected_day = int(drop_down_registration_start_day.get())

        day_of_week_for_selected_day = get_day_of_week_in_japanese(
            this_year, this_month, selected_day
        )
        label_day_of_week_for_registration_start_day.configure(
            text=day_of_week_for_selected_day
        )

    days = []
    for i in range(1, days_of_month + 1, 1):
        days.append(i)

    string_var_registration_start_day = tkinter.StringVar()
    drop_down_registration_start_day = ttk.Combobox(
        tk, state="readonly", width=3, textvariable=string_var_registration_start_day
    )
    drop_down_registration_start_day["values"] = days
    drop_down_registration_start_day.place(x=90, y=200)
    drop_down_registration_start_day.current(0)
    drop_down_registration_start_day.bind(
        "<<ComboboxSelected>>", change_options_for_registration_end_day
    )
    drop_down_registration_start_day.bind(
        "<<ComboboxSelected>>", set_day_of_week_for_registration_start_day, "+"
    )

    day_of_week_for_registration_start_day = get_day_of_week_in_japanese(
        this_year, this_month, 1
    )
    label_day_of_week_for_registration_start_day = tkinter.Label(
        text=day_of_week_for_registration_start_day
    )
    label_day_of_week_for_registration_start_day.place(x=135, y=200)

    label_wave_dash_for_registration_period = tkinter.Label(text="～")
    label_wave_dash_for_registration_period.place(x=165, y=200)

    def change_options_for_registration_start_day(event):
        """設定された登録処理終了日により、登録処理開始日のドロップダウンに適切な値を設定する。"""
        registration_start_days = []
        for i in range(1, int(drop_down_registration_end_day.get()) + 1):
            registration_start_days.append(i)

        drop_down_registration_start_day["values"] = registration_start_days

    def set_day_of_week_for_registration_end_day(event):
        """選択された日に応じた曜日を、処理終了日に設定する。"""
        selected_day = int(drop_down_registration_end_day.get())

        day_of_week_for_selected_day = get_day_of_week_in_japanese(
            this_year, this_month, selected_day
        )
        label_day_of_week_for_registration_end_day.configure(
            text=day_of_week_for_selected_day
        )

    string_var_registration_end_day = tkinter.StringVar()
    drop_down_registration_end_day = ttk.Combobox(
        tk, state="readonly", width=3, textvariable=string_var_registration_end_day
    )
    drop_down_registration_end_day["values"] = days
    drop_down_registration_end_day.place(x=185, y=200)
    drop_down_registration_end_day.current(days_of_month - 1)
    drop_down_registration_end_day.bind(
        "<<ComboboxSelected>>", change_options_for_registration_start_day
    )
    drop_down_registration_end_day.bind(
        "<<ComboboxSelected>>", set_day_of_week_for_registration_end_day, "+"
    )

    day_of_week_for_registration_end_day = get_day_of_week_in_japanese(
        this_year, this_month, days_of_month
    )
    label_day_of_week_for_registration_end_day = tkinter.Label(
        text=day_of_week_for_registration_end_day
    )
    label_day_of_week_for_registration_end_day.place(x=230, y=200)

    CUSTOM_NAVY = "#001f33"
    CUSTOM_ORANGE = "#feb81c"
    register_work_data_button = tkinter.Button(
        tk,
        text="勤務データ登録",
        width=30,
        height=2,
        command=lambda: main(
            entry_staff_id.get(),
            entry_password.get(),
            drop_down_start_hour.get(),
            drop_down_start_minute.get(),
            drop_down_end_hour.get(),
            drop_down_end_minute.get(),
            telecommuting_flag.get(),
            drop_down_registration_start_day.get(),
            drop_down_registration_end_day.get(),
        ),
        foreground=CUSTOM_ORANGE,
        background=CUSTOM_NAVY,
        activeforeground=CUSTOM_NAVY,
        activebackground=CUSTOM_ORANGE,
    )
    register_work_data_button.place(x=20, y=230)

    def reset_values_to_default():
        """入力値を初期値に戻します。"""
        reset_flag = messagebox.askokcancel(
            title="入力値初期化確認", message="入力値を初期値に戻します。", icon="warning"
        )

        if reset_flag is True:
            entry_staff_id.delete(0, tkinter.END)

            entry_password.delete(0, tkinter.END)

            drop_down_start_hour["values"] = hours
            drop_down_start_hour.current(9)

            drop_down_start_minute.current(4)
            drop_down_end_hour["values"] = hours
            drop_down_end_hour.current(18)

            drop_down_end_minute.current(0)

            telecommuting_flag.set(False)

            drop_down_registration_start_day.current(0)

            day_of_week_for_registration_start_day = get_day_of_week_in_japanese(
                this_year, this_month, 1
            )
            label_day_of_week_for_registration_start_day.configure(
                text=day_of_week_for_registration_start_day
            )

            drop_down_registration_end_day["values"] = days
            drop_down_registration_end_day.current(days_of_month - 1)

            day_of_week_for_registration_end_day = get_day_of_week_in_japanese(
                this_year, this_month, days_of_month
            )
            label_day_of_week_for_registration_end_day.configure(
                text=day_of_week_for_registration_end_day
            )
        else:
            return

    clear_button = tkinter.Button(
        tk, text="入力値初期化", command=lambda: reset_values_to_default()
    )
    clear_button.place(x=20, y=280)

    def close_tkinter_window():
        """tkinter の窓を閉じてもいいか確認します。"""
        close_flag = messagebox.askokcancel(
            title="終了確認", message="このアプリを閉じてもいいですか。", icon="question"
        )

        if close_flag is True:
            tk.destroy()
        else:
            return

    close_window_button = tkinter.Button(
        tk, text="閉じる", command=lambda: close_tkinter_window()
    )
    close_window_button.place(x=110, y=280)

    tk.mainloop()


show_tkinter_window()
