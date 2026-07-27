// Live Clock Functionality
function updateClock() {
    const now = new Date();
    const timeOptions = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true };
    const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    
    document.getElementById('live-clock').textContent = now.toLocaleTimeString('en-US', timeOptions);
    document.getElementById('live-date').textContent = now.toLocaleDateString('en-US', dateOptions);
}

setInterval(updateClock, 1000);
updateClock();

// Switch View Role (Admin vs Member)
function switchRole(role) {
    const btnAdmin = document.getElementById('btn-admin-view');
    const btnMember = document.getElementById('btn-member-view');
    
    const title = document.getElementById('welcome-title');
    const subtitle = document.getElementById('welcome-subtitle');
    const kpiTitle = document.getElementById('kpi-dues-title');
    const kpiVal = document.getElementById('kpi-dues-value');
    const kpiSub = document.getElementById('kpi-dues-sub');
    
    if (role === 'admin') {
        btnAdmin.classList.add('active');
        btnMember.classList.remove('active');
        
        title.textContent = 'Dashboard Overview';
        subtitle.innerHTML = 'Logged in as: <strong>Mess Manager Cristiano Messi Junior</strong> (Admin)';
        
        kpiTitle.textContent = 'TOTAL OUTSTANDING DUES';
        kpiVal.textContent = '৳ 9,340.00';
        kpiSub.textContent = 'Collective Member Receivables';
    } else {
        btnMember.classList.add('active');
        btnAdmin.classList.remove('active');
        
        title.textContent = 'Welcome back, Adnan Chowdhury';
        subtitle.innerHTML = 'Logged in as: <strong>Adnan Chowdhury</strong> (Room 302 | S001)';
        
        kpiTitle.textContent = 'ADVANCE BALANCE';
        kpiVal.textContent = '৳ 875.00';
        kpiSub.textContent = 'Outstanding Bill: ৳ 0.00';
    }
}
