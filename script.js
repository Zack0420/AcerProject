// 每個月名稱
const month_names = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];

// 設定閏月的規則
isLeapYear = (year) => {
    return (year % 4 === 0 && year % 100 !== 0 && year % 400 !== 0) || (year % 100 === 0 && year % 400 === 0);
};

// 抓閏月
getFebDays = (year) => {
    return isLeapYear(year) ? 29 : 28;
};

// 抓 calender css
let calender = document.querySelector('.calender');

// 產生年月
generateCalender = (month, year) => {
    let calender_days = calender.querySelector('.calender-days');
    let calender_header_year = calender.querySelector('#year');

    let days_of_month = [31, getFebDays(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    
    calender_days.innerHTML = '';

    let currDate = new Date();
    if (month === undefined) month = currDate.getMonth();
    if (year === undefined) year = currDate.getFullYear();

    let curr_month = `${month_names[month]}`;
    month_picker.innerHTML = curr_month;
    calender_header_year.innerHTML = year;

    let first_day = new Date(year, month, 1);

    for (let i = 0; i <= days_of_month[month] + first_day.getDay() - 1; i++) {
        let day = document.createElement('div');
        if (i >= first_day.getDay()) {
            day.classList.add('calender-day-hover');
            day.innerHTML = i - first_day.getDay() + 1;
            day.innerHTML += `<span></span><span></span><span></span><span></span>`;
            if (i - first_day.getDay() + 1 === currDate.getDate() && year === currDate.getFullYear() && month === currDate.getMonth()) {
                day.classList.add('curr-date');
            }
        }
        calender_days.appendChild(day);
    }
};

// 秀出每個月份
let month_list = calender.querySelector('.month-list');

month_names.forEach((e, index) => {
    let month = document.createElement('div');
    month.innerHTML = `<div date-month="${index}">${e}</div>`;
    
    month.querySelector('div').onclick = () => {
        month_list.classList.remove('show');
        curr_month.value = index;
        generateCalender(index, curr_year.value);
    };
    month_list.appendChild(month);
});

// 按下個月份按鈕的時候會跳出各個月份
let month_picker = calender.querySelector('#month-picker');

month_picker.onclick = () => {
    month_list.classList.add('show');
};

let currDate = new Date();

let curr_month = { value: currDate.getMonth() };
let curr_year = { value: currDate.getFullYear() };

generateCalender(curr_month.value, curr_year.value);

document.querySelector('#prev-year').onclick = () => {
    --curr_year.value;
    generateCalender(curr_month.value, curr_year.value);
};

document.querySelector('#next-year').onclick = () => {
    ++curr_year.value;
    generateCalender(curr_month.value, curr_year.value);
};


const trips = [
    {
    id: 1,
    title: '東京自由行',
    startDate: '2023-05-10',
    endDate: '2023-05-15',
    itinerary: [
        {
        date: '2023-05-10',
        schedule: '上午抵達東京,入住hotel'
        },
    {
        date: '2023-05-11',
        schedule: '淺草寺、晴空塔'
    },
        // ... 其他日期行程
    ]
    },
    // ... 其他行程
    ];

function renderTripInfo(trip) {
const $tripInfo = $('.trip-info');
$tripInfo.empty(); // 清空之前的內容
$tripInfo.append(`
    <h2>${trip.title}</h2>
    <p>旅程日期: ${trip.startDate} - ${trip.endDate}</p>
    <!-- 您可以在這裡加入更多行程資訊 -->
`);
}


function renderDailySchedule(trip) {
const $dailySchedule = $('.daily-schedule');
$dailySchedule.empty(); // 清空之前的內容

trip.itinerary.forEach((day, index) => {
    const $accordionItem = $(`
    <div class="accordion-item">
        <h2 class="accordion-header" id="heading${index}">
        <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${index}" aria-expanded="false" aria-controls="collapse${index}">
            ${day.date}
        </button>
        </h2>
        <div id="collapse${index}" class="accordion-collapse collapse" aria-labelledby="heading${index}" data-bs-parent="#accordionExample">
        <div class="accordion-body">
            ${day.schedule}
        </div>
        </div>
    </div>
    `);
    $dailySchedule.append($accordionItem);
});
}