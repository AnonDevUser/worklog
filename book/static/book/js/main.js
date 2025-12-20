document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const shiftListBody = document.getElementById('shift-list-body');
    const mobileShiftList = document.getElementById('mobile-shift-list');

    const addShiftBtn = document.getElementById('add-shift-btn');
    const summaryBtn = document.getElementById('summary-btn');
    const mobileSummaryBtn = document.getElementById('mobile-summary-btn');

    const summaryModal = document.getElementById('summary-modal');
    const closeSummary = document.getElementById('close-summary');

    const formModal = document.getElementById('form-modal');
    const closeForm = document.getElementById('close-form');
    const shiftForm = document.getElementById('shift-data-form');
    const formTitle = document.getElementById('form-title');

    // Modal Toggles
    function toggleModal(modal, show = true) {
        if (show) {
            modal.classList.add('active');
        } else {
            modal.classList.remove('active');
        }
    }

    [summaryBtn, mobileSummaryBtn].forEach(btn => {
        if (btn) btn.addEventListener('click', () => {
            fetchSummary();
            toggleModal(summaryModal);

            // Auto-close mobile side nav if it's open
            const sideNav = document.getElementById('side-nav');
            const navOverlay = document.getElementById('nav-overlay');
            const menuToggle = document.getElementById('menu-toggle');
            if (sideNav && sideNav.classList.contains('active')) {
                sideNav.classList.remove('active');
                navOverlay.classList.remove('active');
                menuToggle.classList.remove('open');
            }
        });
    });

    closeSummary.addEventListener('click', () => toggleModal(summaryModal, false));
    summaryModal.addEventListener('click', (e) => {
        if (e.target === summaryModal) toggleModal(summaryModal, false);
    });

    addShiftBtn.addEventListener('click', () => {
        formTitle.textContent = 'Log New Shift';
        shiftForm.reset();
        document.getElementById('shift-id').value = '';
        toggleModal(formModal);
    });

    closeForm.addEventListener('click', () => toggleModal(formModal, false));
    formModal.addEventListener('click', (e) => {
        if (e.target === formModal) toggleModal(formModal, false);
    });

    // Helper: CSRF Token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Dummy Data for UI Check
    const dummyShifts = [
        {
            id: 101,
            start_time: "2023-12-20T03:00:00",
            end_time: "2023-12-20T10:00:00",
            hourly_rate: "23.50",
            earnings: "164.50",
            job: "Dog walking",
            is_settled: false,
            break_duration: 0
        },
        {
            id: 102,
            start_time: "2023-12-21T09:00:00",
            end_time: "2023-12-21T17:00:00",
            hourly_rate: "25.00",
            earnings: "200.00",
            job: "Content Writing",
            is_settled: true,
            break_duration: 30
        },
        {
            id: 103,
            start_time: "2023-12-22T14:00:00",
            end_time: "2023-12-22T18:00:00",
            hourly_rate: "20.00",
            earnings: "80.00",
            job: "Social Media Mgmt",
            is_settled: false,
            break_duration: 0
        }
    ];

    // Initial Fetch
    // fetchShifts();
    renderShifts(dummyShifts);

    // Fetch Shifts
    async function fetchShifts() {
        try {
            const response = await fetch('/api/shifts/');
            if (!response.ok) throw new Error('Failed to fetch shifts');
            const data = await response.json();
            // renderShifts(data); // Uncomment to use real data
        } catch (error) {
            console.error(error);
            // Render dummy data on error too so it looks good
            renderShifts(dummyShifts);
        }
    }

    // Render Shifts (Dual View)
    function renderShifts(shifts) {
        if (shifts.length === 0) {
            const emptyMsg = 'No shifts logged yet.';
            shiftListBody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-secondary); padding: 5rem;">${emptyMsg}</td></tr>`;
            mobileShiftList.innerHTML = `<p style="text-align: center; color: var(--text-secondary); padding: 5rem;">${emptyMsg}</p>`;
            return;
        }

        // Render Desktop Table
        shiftListBody.innerHTML = shifts.map((shift, index) => `
            <tr data-id="${shift.id}">
                <td style="color: var(--text-secondary);">${index + 1}.</td>
                <td>${formatDate(shift.start_time)}</td>
                <td>${formatTimeShort(shift.start_time)}</td>
                <td>${formatTimeShort(shift.end_time)}</td>
                <td>$${shift.hourly_rate}</td>
                <td>
                    $${shift.earnings}
                    ${!shift.is_settled ? '<span class="badge badge-due">DUE</span>' : ''}
                </td>
                <td>${shift.notes || shift.job || '---'}</td>
                <td style="text-align: right;">
                    <div class="action-btns">
                        <button class="btn-text" onclick="settleShift(${shift.id})">Settle</button>
                        <button class="btn-text" onclick="prepareEdit(${shift.id})">Edit</button>
                        <button class="btn-text btn-delete" onclick="deleteShift(${shift.id})">Delete</button>
                    </div>
                </td>
            </tr>
        `).join('');

        // Render Mobile Cards (Creative View)
        mobileShiftList.innerHTML = shifts.map((shift) => `
            <div class="mobile-shift-card" data-id="${shift.id}">
                <div class="card-header">
                    <span class="card-date">${formatDate(shift.start_time)}</span>
                    <span class="card-pay">$${shift.earnings}</span>
                </div>
                <div class="card-body">
                    <p class="card-job">${shift.job || shift.notes || 'Unnamed Job'}</p>
                    <p class="card-times">${formatTimeShort(shift.start_time)} → ${formatTimeShort(shift.end_time)} ($${shift.hourly_rate}/h)</p>
                </div>
                <div class="card-footer">
                    <div>
                        ${!shift.is_settled ? '<span class="badge badge-due">Awaiting Payment</span>' : '<span style="color: var(--accent-color); font-size: 0.7rem; font-weight: 700;">PAID</span>'}
                    </div>
                    <div class="action-btns">
                        <button class="btn-text" onclick="settleShift(${shift.id})">Settle</button>
                        <button class="btn-text" onclick="prepareEdit(${shift.id})">Edit</button>
                        <button class="btn-text btn-delete" onclick="deleteShift(${shift.id})">Delete</button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Fetch Summary
    async function fetchSummary() {
        // Dummy Summary Data for UI Check
        const dummySummary = {
            total_hours: 44.50,
            total_earnings: 1112.50,
            today_hours: 8.00,
            week_hours: 40.00
        };

        const updateUI = (data) => {
            document.getElementById('modal-total-hours').textContent = data.total_hours.toFixed(2);
            document.getElementById('modal-total-earnings').textContent = `$${data.total_earnings.toFixed(2)}`;
            document.getElementById('modal-today-hours').textContent = `${data.today_hours.toFixed(2)}h`;
            document.getElementById('modal-week-hours').textContent = `${data.week_hours.toFixed(2)}h`;
        };

        // Render dummy data immediately
        updateUI(dummySummary);

        try {
            const response = await fetch('/api/shifts/summary/');
            if (!response.ok) throw new Error('Failed to fetch summary');
            const data = await response.json();
            // updateUI(data); // Uncomment to use real data
        } catch (error) {
            console.error(error);
            // Already showing dummy data
        }
    }

    // Form Submission (Add/Edit)
    shiftForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(shiftForm);
        const id = formData.get('id');
        const data = Object.fromEntries(formData.entries());

        const method = id ? 'PATCH' : 'POST';
        const url = id ? `/api/shifts/${id}/` : '/api/shifts/';

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                toggleModal(formModal, false);
                fetchShifts();
            } else {
                const errorData = await response.json();
                alert(errorData.detail || 'Error saving shift');
            }
        } catch (error) {
            alert('Network error');
        }
    });

    // Prepare Edit
    window.prepareEdit = async (id) => {
        let shift;
        try {
            const response = await fetch(`/api/shifts/${id}/`);
            if (response.ok) {
                shift = await response.json();
            }
        } catch (error) {
            console.warn('API fetch failed, checking dummy data');
        }

        // Fallback to dummy data if API failed or returned error
        if (!shift) {
            shift = dummyShifts.find(s => s.id === id);
        }

        if (shift) {
            formTitle.textContent = 'Edit Shift';
            document.getElementById('shift-id').value = shift.id;
            document.getElementById('job-input').value = shift.job || shift.notes || '';
            document.getElementById('start-time-input').value = shift.start_time.slice(0, 16);
            document.getElementById('end-time-input').value = shift.end_time.slice(0, 16);
            document.getElementById('hourly-rate-input').value = shift.hourly_rate;
            document.getElementById('break-input').value = shift.break_duration || 0;

            toggleModal(formModal);
        } else {
            alert('Error loading shift details');
        }
    };

    // Delete Shift
    window.deleteShift = async (id) => {
        if (!confirm('Are you sure you want to delete this shift?')) return;

        try {
            const response = await fetch(`/api/shifts/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken
                }
            });

            if (response.ok) {
                fetchShifts();
            }
        } catch (error) {
            alert('Error deleting shift');
        }
    };

    // Settle Shift
    window.settleShift = async (id) => {
        try {
            const response = await fetch(`/api/shifts/${id}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ is_settled: true })
            });
            if (response.ok) {
                fetchShifts();
            }
        } catch (error) {
            console.error(error);
        }
    };

    // Helpers
    function formatDate(dateStr) {
        const d = new Date(dateStr);
        return `${d.getFullYear()}/${(d.getMonth() + 1).toString().padStart(2, '0')}/${d.getDate().toString().padStart(2, '0')}`;
    }

    function formatTimeShort(dateStr) {
        const d = new Date(dateStr);
        let hours = d.getHours();
        const ampm = hours >= 12 ? 'pm' : 'am';
        hours = hours % 12;
        hours = hours ? hours : 12;
        return `${hours} ${ampm}`;
    }
});
