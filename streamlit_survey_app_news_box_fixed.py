import os
import random
import time
import html
from datetime import datetime
from collections import Counter

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


st.set_page_config(
    page_title="Анкета: практики найма молодых специалистов",
    page_icon="📝",
    layout="centered",
)

SHEET_NAME = "diploma"
WORKSHEET_NAME = "result"

RESPONDENT_GROUPS = [
    "Контрольная группа",
    "Тестовая группа 1",
    "Тестовая группа 2",
]

BASE_CITY_OPTIONS = [
    "Москва",
    "Санкт-Петербург",
    "Новосибирск",
    "Екатеринбург",
    "Казань",
    "Другой город",
]

BASE_COMPANY_SPHERES = [
    "IT",
    "Финансы",
    "Связь / телекоммуникации",
    "Реклама / маркетинг",
    "Торговля (оптовая и розничная)",
    "Другое",
]

AGREEMENT_OPTIONS = [
    "1 — Полностью НЕ согласен(-на)",
    "2 — Скорее НЕ согласен(-на)",
    "3 — Ни да, ни нет",
    "4 — Скорее согласен(-на)",
    "5 — Полностью согласен(-на)",
]

NEWS_TEXT_1 = """
Высшее образование по-новому: каким может стать российский университет

Специальный корреспондент

Обсуждение необходимости изменений в системе высшего образования в России шло не один год — от претензий к формальности дипломов до вопросов о реальной готовности выпускников к работе. Теперь этот запрос начинает получать практическое воплощение. Реформа пока не запущена в полном объеме, но ее контуры уже обозначены: в ряде вузов стартовали пилотные проекты, которые позволяют в управляемом и поэтапном режиме проверить будущую модель перед масштабированием на всю систему.

В основе предлагаемых изменений — попытка соединить два подхода. С одной стороны, речь идет о возвращении к сильным сторонам советской высшей школы с ее глубокой теоретической подготовкой. С другой — о внедрении современных практических форматов. В итоге модель выстраивается так, чтобы студент не только получал фундаментальные знания, но и учился применять их в реальных задачах. Логика обучения постепенно смещается к тому, чтобы выпускник мог сразу включаться в профессиональную деятельность, без длительной адаптации на рабочем месте.

Такой подход требует и большей гибкости самой системы. В рамках пилотов уже просматривается отход от универсальных шаблонов: программы адаптируются под требования конкретных отраслей. Подготовка инженеров, медиков или IT-специалистов все больше учитывает специфику их будущей работы.

В более широком смысле реформа ориентирована на формирование национальной модели высшего образования, связанной с внутренними потребностями экономики. Университеты должны готовить специалистов для тех сфер, где существует устойчивый спрос внутри страны. Это отражается и в изменении логики квалификаций: они становятся более понятными для работодателей, поскольку напрямую связаны с набором конкретных компетенций.

Такая переориентация рассматривается как часть более масштабной задачи — укрепления технологического суверенитета. Подготовка кадров становится ключевым элементом развития собственных научных и инженерных решений. Университет в этой системе выступает не только как образовательная площадка, но и как важное звено технологического развития.

При этом новая модель не предполагает изоляции. Сохраняется сопоставимость образовательных программ, а международное сотрудничество остается важной частью университетской жизни. Речь идет скорее о смене позиции — от заимствования готовых форматов к выстраиванию взаимодействия на основе собственных стандартов.

Пока все эти изменения существуют в формате пилотных решений и концепций. Однако уже сейчас можно говорить о формировании новой логики высшего образования — более глубокой, практикоориентированной и связанной с задачами развития страны. Насколько успешно она будет реализована, станет ясно по мере того, как экспериментальные подходы выйдут за пределы отдельных университетов.
"""

NEWS_TEXT_2 = """
Реформа без ясного курса: почему изменения в высшем образовании вызывают вопросы

Специальный корреспондент

От пилотных проектов реформы высшего образования ждали ясности — как именно будет устроена новая система и к чему готовиться университетам. Но пока происходит обратное: чем дальше идет обсуждение, тем больше возникает вопросов. Четкой стратегии по-прежнему не видно, сроки переносятся, формулировки меняются, а сами решения выглядят как набор разрозненных инициатив.

В такой ситуации вузы оказываются в подвешенном состоянии. Им приходится перестраиваться под новые требования, заполнять отчеты и вводить изменения, не понимая конечной цели. Растет бюрократическая нагрузка, ресурсы уходят на адаптацию к постоянно меняющимся правилам, а не на развитие обучения и науки. При этом реальные проблемы университетов остаются в стороне: вопросы финансирования, кадров и инфраструктуры обсуждаются значительно реже.

Сама идея реформы также вызывает вопросы. По сути, предлагается вернуться к модели, во многом напоминающей советскую систему образования. Однако за последние десятилетия существенно изменились экономика, наука и требования к специалистам, поэтому такой поворот для части экспертов выглядит скорее шагом назад.

Много говорится о сближении образования с потребностями экономики. Однако пока это скорее декларация, чем рабочая модель: неясно, как будет выстроено взаимодействие с работодателями, а на фоне курса на возврат к советской системе возникает риск, что эта связь не усилится, а, напротив, ослабнет. Дополнительный риск связан с неопределенностью на рынке труда: работодатели только привыкли к системе бакалавриата и магистратуры, а теперь им придется заново разбираться в квалификациях.

Одновременно возникает риск утраты уже достигнутого. За последние годы университеты выстроили международные связи, запустили совместные программы, интегрировались в глобальное образовательное пространство. Резкое изменение курса может обнулить эти наработки без равноценной замены, сокращая возможности для студентов учиться и получать опыт за рубежом и в целом отдаляя систему высшего образования от сложившихся международных стандартов.

В итоге создается впечатление, что за громкими заявлениями скрывается в значительной степени формальное переименование уровней образования без глубоких содержательных изменений. Такая трансформация не только не решает накопившиеся проблемы, но и способна усугубить их, усиливая неопределенность и дополнительно нагружая систему.
"""

BASE_STATEMENTS = [
    "Наличие диплома будет говорить о хорошем знании теории в профессиональной области",
    "Диплом будет означать готовность выполнять реальные рабочие задачи",
    "Наличие диплома будет говорить о том, что кандидату не требуется дополнительное обучение необходимым для работы навыкам",
    "Высшее образование будет формировать у кандидатов готовность работать с современными технологиями и инструментами",
    "Наличие диплома будет говорить о том, что уровень подготовки кандидата соответствует международным требованиям",
    "По диплому будет легко понять, какими профессиональными навыками обладает кандидат",
]

AGE_OPTIONS = [
    "Менее 18",
    "18-24 года",
    "25-34 года",
    "35-44 года",
    "Более 45",
]

EDUCATION_OPTIONS = [
    "Закончено 9 классов и меньше (неполное среднее)",
    "Закончено 11 классов школы (среднее общее)",
    "Закончено училище/техникум/колледж (среднее специальное)",
    "Получаю высшее образование (неоконченное высшее)",
    "Есть диплом о высшем образовании",
    "Есть 2 диплома о высшем образовании/ученая степень",
]

EXPERIENCE_OPTIONS = [
    "Менее года",
    "1-3 года",
    "3-5 лет",
    "5-10 лет",
    "Более 10 лет",
]


def get_gspread_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    if "gcp_service_account" not in st.secrets:
        raise RuntimeError(
            "Не найдены credentials в st.secrets['gcp_service_account']. "
            "Добавьте сервисный аккаунт в secrets.toml."
        )

    credentials_info = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    return gspread.authorize(creds)


@st.cache_resource
def get_worksheet():
    client = get_gspread_client()
    spreadsheet = client.open(SHEET_NAME)
    try:
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=100)
        worksheet.append_row(get_headers(), value_input_option="USER_ENTERED")
    return worksheet


def get_headers():
    return [
        "duration_seconds",
        "submitted_at",
        "respondent_group",
        "screenout_reason",
        "city",
        "employment_status",
        "recruitment_last_12m",
        "recruitment_experience",
        "company_sphere",
        "reform_understanding",
        "news_variant_shown",
        "stmt_1",
        "stmt_2",
        "stmt_3",
        "stmt_4",
        "stmt_5",
        "stmt_6",
        "stmt_7",
        "stmt_8",
        "gender",
        "age",
        "education",
        "work_experience",
    ]


def ensure_headers():
    ws = get_worksheet()
    values = ws.get_all_values()
    if not values:
        ws.append_row(get_headers(), value_input_option="USER_ENTERED")
        return

    existing_headers = values[0]
    expected_headers = get_headers()
    if existing_headers != expected_headers:
        ws.clear()
        ws.append_row(expected_headers, value_input_option="USER_ENTERED")
        if len(values) > 1:
            for row in values[1:]:
                padded = row + [""] * (len(expected_headers) - len(row))
                ws.append_row(padded[: len(expected_headers)], value_input_option="USER_ENTERED")


def get_existing_group_counts() -> Counter:
    try:
        ws = get_worksheet()
        records = ws.get_all_records()
        counts = Counter()
        for record in records:
            group = str(record.get("respondent_group", "")).strip()
            if group in RESPONDENT_GROUPS:
                counts[group] += 1
        for group in RESPONDENT_GROUPS:
            counts[group] += 0
        return counts
    except Exception:
        return Counter({group: 0 for group in RESPONDENT_GROUPS})


def assign_respondent_group() -> str:
    counts = get_existing_group_counts()
    min_count = min(counts.values())
    candidates = [group for group, cnt in counts.items() if cnt == min_count]
    return random.choice(candidates)


def append_response(response: dict):
    ensure_headers()
    ws = get_worksheet()
    row = [response.get(col, "") for col in get_headers()]
    ws.append_row(row, value_input_option="USER_ENTERED")


def init_state():
    defaults = {
        "submitted": False,
        "screened_out": False,
        "screenout_reason": "",
        "respondent_group": None,
        "assigned_group": None,
        "page": 0,
        "city_options": None,
        "company_sphere_options": None,
        "statement_order": None,
        "start_time": datetime.utcnow(),
        "answers": {
            "city": None,
            "employment_status": None,
            "recruitment_last_12m": None,
            "recruitment_experience": None,
            "company_sphere": None,
            "reform_understanding": None,
            "news_variant_shown": "Не показывалось",
            "statement_answers": {},
            "gender": None,
            "age": None,
            "education": None,
            "work_experience": None,
        },
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.city_options is None:
        base = BASE_CITY_OPTIONS.copy()
        other = "Другой город"
        shuffled = [x for x in base if x != other]
        random.shuffle(shuffled)
        shuffled.append(other)
        st.session_state.city_options = shuffled

    if st.session_state.company_sphere_options is None:
        base = BASE_COMPANY_SPHERES.copy()
        other = "Другое"
        shuffled = [x for x in base if x != other]
        random.shuffle(shuffled)
        shuffled.append(other)
        st.session_state.company_sphere_options = shuffled

    if st.session_state.statement_order is None:
        statements = BASE_STATEMENTS.copy()
        random.shuffle(statements)
        st.session_state.statement_order = statements


def screenout(reason: str):
    st.session_state.screened_out = True
    st.session_state.screenout_reason = reason


def clear_screenout():
    st.session_state.screened_out = False
    st.session_state.screenout_reason = ""


def save_and_next(field_name: str, value):
    st.session_state.answers[field_name] = value
    st.session_state.page += 1
    st.rerun()


def back_page():
    if st.session_state.page > 0:
        st.session_state.page -= 1
        st.rerun()


def render_navigation(can_go_next: bool, next_label: str = "Далее", force_enable_next: bool = False):
    col1, col2 = st.columns(2)
    back_clicked = False
    next_clicked = False
    with col1:
        if st.session_state.page > 0:
            back_clicked = st.button("Назад", use_container_width=True)
    with col2:
        next_clicked = st.button(
            next_label,
            use_container_width=True,
            disabled=(not can_go_next) and (not force_enable_next),
        )

    if back_clicked:
        back_page()
    return next_clicked


def render_intro_page():
    st.title("Анкета: практики найма молодых специалистов")
    st.write("Здравствуйте!")
    st.write("Приглашаем вас принять участие в исследовании, посвященном практикам найма молодых специалистов.")
    st.info(
        "Опрос анонимный и займет не более 10 минут. Пожалуйста, заполняйте анкету внимательно и последовательно. "
        "В ней нет правильных или неправильных ответов — важно ваше мнение."
    )
    st.error("Пожалуйста, выключите VPN для корректной работы анкеты.")

    if render_navigation(True):
        st.session_state.page = 1
        st.rerun()


def render_screenout_message():
    st.success("Спасибо за участие!")


def render_news_message(news_text: str):
    """Показывает новостной текст в визуально выделенной рамке."""
    st.markdown("**Прочитайте внимательно новостное сообщение**")
    st.markdown(
        """
        <style>
            .news-box {
                border: 1.5px solid #c9ced6;
                border-radius: 12px;
                padding: 22px 24px;
                margin: 12px 0 20px 0;
                background-color: #ffffff;
                color: #1f2937 !important;
                box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
                line-height: 1.6;
                font-size: 16px;
            }
            .news-box p {
                margin: 0 0 14px 0;
                color: #1f2937 !important;
            }
            .news-box p:first-child {
                font-size: 20px;
                font-weight: 700;
                line-height: 1.35;
                margin-bottom: 16px;
                color: #111827 !important;
            }
            .news-box p:nth-child(2) {
                font-style: italic;
                color: #4b5563 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    paragraphs = [part.strip() for part in news_text.strip().split("\n\n") if part.strip()]
    body = "".join(f"<p>{html.escape(paragraph).replace(chr(10), '<br>')}</p>" for paragraph in paragraphs)
    st.markdown(f'<div class="news-box">{body}</div>', unsafe_allow_html=True)


def save_screenout_and_finish(reason: str):
    screenout(reason)
    st.session_state.submitted = True



def submit_full_response():
    end_time = datetime.utcnow()
    start_time = st.session_state.start_time
    duration_seconds = (end_time - start_time).total_seconds()
    a = st.session_state.answers
    respondent_group = st.session_state.assigned_group or assign_respondent_group()
    st.session_state.respondent_group = respondent_group

    ordered_statement_answers = {f"stmt_{i+1}": "" for i in range(8)}
    for idx, statement in enumerate(BASE_STATEMENTS, start=1):
        ordered_statement_answers[f"stmt_{idx}"] = a["statement_answers"].get(statement, "")

    response = {
        "duration_seconds": duration_seconds,
        "submitted_at": datetime.utcnow().isoformat(),
        "respondent_group": respondent_group,
        "screenout_reason": "",
        "city": a["city"],
        "employment_status": a["employment_status"],
        "recruitment_last_12m": a["recruitment_last_12m"],
        "recruitment_experience": a["recruitment_experience"],
        "company_sphere": a["company_sphere"],
        "reform_understanding": a["reform_understanding"],
        "news_variant_shown": a["news_variant_shown"],
        **ordered_statement_answers,
        "gender": a["gender"],
        "age": a["age"],
        "education": a["education"],
        "work_experience": a["work_experience"],
    }
    append_response(response)
    st.session_state.submitted = True


def main():
    init_state()

    if st.session_state.submitted:
        if st.session_state.screened_out:
            render_screenout_message()
            st.info("Скрининговые ответы сохранены.")
        else:
            st.success("Спасибо! Ваш ответ успешно сохранён.")
            st.caption("Ответ записан в Google Sheets.")
        st.stop()

    page = st.session_state.page
    answers = st.session_state.answers

    if page == 0:
        render_intro_page()

    elif page == 1:
        st.write("**В каком городе вы проживаете постоянно (не менее 6 месяцев в году)?**")
        current = answers["city"]
        city = st.radio(
            "",
            st.session_state.city_options,
            index=st.session_state.city_options.index(current) if current in st.session_state.city_options else None,
            label_visibility="collapsed",
        )
        if render_navigation(city is not None):
            answers["city"] = city
            if city != "Москва":
                save_screenout_and_finish("Респондент проживает не в Москве")
            else:
                st.session_state.page += 1
            st.rerun()

    elif page == 2:
        st.write("**Вы работаете или не работаете?**")
        options = ["Работаю (в том числе, неполный рабочий день)", "Не работаю"]
        current = answers["employment_status"]
        value = st.radio("", options, index=options.index(current) if current in options else None, label_visibility="collapsed")
        if render_navigation(value is not None):
            answers["employment_status"] = value
            if value == "Не работаю":
                save_screenout_and_finish("Респондент не работает")
            else:
                st.session_state.page += 1
            st.rerun()

    elif page == 3:
        st.write("**Участвовали ли вы в подборе студентов и недавних выпускников за последние 12 месяцев?**")
        options = ["Да, регулярно", "Да, несколько раз", "Нет"]
        current = answers["recruitment_last_12m"]
        value = st.radio("", options, index=options.index(current) if current in options else None, label_visibility="collapsed")
        if render_navigation(value is not None):
            answers["recruitment_last_12m"] = value
            if value == "Нет":
                save_screenout_and_finish("Не участвовал в подборе студентов и выпускников за последние 12 месяцев")
            else:
                st.session_state.page += 1
            st.rerun()

    elif page == 4:
        st.write("**Как давно вы вовлечены в процесс найма студентов и недавних выпускников?**")
        options = ["Более 3 лет", "1-3 года", "Менее 1 года"]
        current = answers["recruitment_experience"]
        value = st.radio("", options, index=options.index(current) if current in options else None, label_visibility="collapsed")
        if render_navigation(value is not None):
            answers["recruitment_experience"] = value
            if value == "Менее 1 года":
                save_screenout_and_finish("Опыт найма студентов и выпускников менее 1 года")
            else:
                st.session_state.page += 1
            st.rerun()

    elif page == 5:
        st.write("**К какой сфере относится компания, в которой вы работаете?**")
        current = answers["company_sphere"]
        options = st.session_state.company_sphere_options
        value = st.radio(
            "",
            options,
            index=options.index(current) if current in options else None,
            label_visibility="collapsed",
        )
        if render_navigation(value is not None):
            answers["company_sphere"] = value
            if st.session_state.assigned_group is None:
                st.session_state.assigned_group = assign_respondent_group()
            st.session_state.page += 1
            st.rerun()

    elif page == 6:
        st.write("**В последние годы в России началась реформа системы высшего образования. Насколько хорошо вы понимаете содержание реформы?**")
        st.markdown("_Оцените по шкале от 1 до 5, где 1 — совсем НЕ понимаю, а 5 — полностью понимаю содержание реформы._")
        options = [
            "1 — Совсем НЕ понимаю содержание реформы",
            "2",
            "3",
            "4",
            "5 — Полностью понимаю содержание реформы",
        ]
        current = answers["reform_understanding"]
        value = st.radio("", options, index=options.index(current) if current in options else None, label_visibility="collapsed")
        if render_navigation(value is not None):
            answers["reform_understanding"] = value
            group = st.session_state.assigned_group
            if group == "Тестовая группа 1":
                answers["news_variant_shown"] = "Новостное сообщение 1"
            elif group == "Тестовая группа 2":
                answers["news_variant_shown"] = "Новостное сообщение 2"
            else:
                answers["news_variant_shown"] = "Не показывалось"
            st.session_state.page += 1
            st.rerun()

    elif page == 7:
        # Экран с инструкцией перед новостью
        if answers["news_variant_shown"] != "Не показывалось":
            st.write("Сейчас мы покажем вам новостное сообщение. Прочитайте его внимательно.")
            if render_navigation(True):
                st.session_state.page += 1
                st.rerun()
        else:
            st.session_state.page += 2
            st.rerun()

    elif page == 8:
        # Экран с новостью и таймером
        if answers["news_variant_shown"] == "Новостное сообщение 1":
            render_news_message(NEWS_TEXT_1)
        elif answers["news_variant_shown"] == "Новостное сообщение 2":
            render_news_message(NEWS_TEXT_2)
        else:
            st.session_state.page += 1
            st.rerun()

        if "news_start_time" not in st.session_state or st.session_state.news_start_time is None:
            st.session_state.news_start_time = datetime.utcnow()

        elapsed = (datetime.utcnow() - st.session_state.news_start_time).total_seconds()
        next_enabled = elapsed >= 20

        if render_navigation(next_enabled):
            st.session_state.news_start_time = None
            st.session_state.page += 1
            st.rerun()

        if not next_enabled:
            time.sleep(1)
            st.rerun()

    elif page == 9:
        st.write(
            "**Посмотрите на высказывания других людей о том, что диплом о высшем образовании будет говорить о кандидатах ПОСЛЕ РЕФОРМЫ ВЫСШЕГО ОБРАЗОВАНИЯ. Насколько вы согласны или не согласны с каждым из них?**"
        )
        st.caption(
            "Отвечайте, исходя из того, как это будет в будущем, после реализации реформы, а не как это обстоит сейчас"
        )

        all_answered = True
        temp_answers = answers["statement_answers"].copy()

        for statement in st.session_state.statement_order:
            current = temp_answers.get(statement)
            value = st.radio(
                statement,
                AGREEMENT_OPTIONS,
                index=AGREEMENT_OPTIONS.index(current) if current in AGREEMENT_OPTIONS else None,
                key=f"stmt_{statement}",
            )
            temp_answers[statement] = value
            if not value:
                all_answered = False

        if render_navigation(all_answered):
            answers["statement_answers"] = temp_answers
            st.session_state.page += 1
            st.rerun()

    elif page == 10:
        st.write("**Укажите ваш пол.**")
        options = ["Мужчина", "Женщина"]
        current = answers["gender"]
        value = st.radio("", options, index=options.index(current) if current in options else None, label_visibility="collapsed")
        if render_navigation(value is not None):
            save_and_next("gender", value)

    elif page == 11:
        st.write("**Сколько вам полных лет?**")
        current = answers["age"]
        value = st.radio("", AGE_OPTIONS, index=AGE_OPTIONS.index(current) if current in AGE_OPTIONS else None, label_visibility="collapsed")
        if render_navigation(value is not None):
            save_and_next("age", value)

    elif page == 12:
        st.write("**Какое у вас образование?**")
        current = answers["education"]
        value = st.radio("", EDUCATION_OPTIONS, index=EDUCATION_OPTIONS.index(current) if current in EDUCATION_OPTIONS else None, label_visibility="collapsed")
        if render_navigation(value is not None):
            save_and_next("education", value)

    elif page == 13:
        st.write("**Какой у вас стаж работы в текущей профессиональной деятельности?**")
        current = answers["work_experience"]
        value = st.radio("", EXPERIENCE_OPTIONS, index=EXPERIENCE_OPTIONS.index(current) if current in EXPERIENCE_OPTIONS else None, label_visibility="collapsed")
        if render_navigation(value is not None, next_label="Отправить"):
            answers["work_experience"] = value
            submit_full_response()
            st.rerun()


if __name__ == "__main__":
    main()
