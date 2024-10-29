# 🎓 School Management System

A comprehensive school management system designed for managing academic, administrative, and student/teacher information. Built with Django REST API for the backend and React for the frontend, this system enables streamlined handling of school operations, student performance, notifications, aamarupay payment getway method and attendance management.

## 🚀 Live Demo

- **Frontend**: [Amader CST (Netlify)](https://amader-cst.netlify.app)
- **Backend API Documentation**: [API Endpoints](https://github.com/Md-Merazul-Islam/School-Management-Front-End/blob/main/imporant.text)

## 🔑 Access

| Role    | Username | Password   |
| ------- | -------- | ---------- |
| Admin   | `meraz`  | `meraz2004`|
| user | `ratin`  | `meraz2004`|




## 📂 Repository Links

- **Frontend GitHub Repository**: [School Management Front-End](https://github.com/Md-Merazul-Islam/School-Management-Front-End)
- **Backend GitHub Repository**: [School Management Backend](https://github.com/Md-Merazul-Islam/School-Management-Website-Backend)



## 📱 Key Features

- **Authentication**: Secure login/logout
- **Profile Management**: Students & teachers
- **Exam Results**: Track & grading
- **Monthly fees pay** : Aamarupay payment getway method
- **GPA Calculation**: Automated GPA
- **Activity Management**: Events & tracking
- **Attendance**: Tracking & alerts
- **Notice Board**: Dynamic updates
- **Notifications**: SMS & email alerts
- **Reports**: Generate & download
- **Admin Panel**: Manage settings
- **Data Security**: Authentication & encryption



## 🛠️ Technologies Used

### Backend
- **Framework**: Django REST API for API management and backend logic.
- **Database**: PostgreSQL for reliable data management.
- **Monitoring**: Coros Check for performance and security.



---

## 📚 API Endpoints

### Account Management
| Action               | Endpoint                                                                       |
|----------------------|--------------------------------------------------------------------------------|
| All Users            | [`/user/allUser/`](https://school-management-five-iota.vercel.app/accounts/)   |
| Register             | [`/register`](https://school-management-five-iota.vercel.app/accounts/register/) |
| Login                | [`/login`](https://school-management-five-iota.vercel.app/accounts/login/)     |
| Logout               | [`/logout`](https://school-management-five-iota.vercel.app/accounts/logout/)   |
| User Details         | [`/profiles`](https://school-management-five-iota.vercel.app/accounts/profiles/)|
| User Role Check      | [`/is_users_staff`](https://school-management-five-iota.vercel.app/accounts/is_users_staff/) |

### Academics
| Action               | Endpoint                                                                       |
|----------------------|--------------------------------------------------------------------------------|
| Students             | [`/students/`](https://school-management-five-iota.vercel.app/academics/students/) |
| Teachers             | [`/teachers/`](https://school-management-five-iota.vercel.app/academics/teachers/) |
| Student List         | [`/students-list`](https://school-management-five-iota.vercel.app/academics/students-list/) |
| Teacher List         | [`/teachers-list`](https://school-management-five-iota.vercel.app/academics/teachers-list/) |
| Classes              | [`/classes`](https://school-management-five-iota.vercel.app/academics/classes/) |
| Subjects             | [`/subjects`](https://school-management-five-iota.vercel.app/academics/subjects/) |
| Notices              | [`/notices`](https://school-management-five-iota.vercel.app/academics/notices/) |

### Class Attendance & Marks
| Action               | Endpoint                                                                       |
|----------------------|--------------------------------------------------------------------------------|
| Attendance List      | [`/attendance-check`](https://school-management-five-iota.vercel.app/classes/attendance-check/) |
| Marks                | [`/marks`](https://school-management-five-iota.vercel.app/classes/marks/)      |

### Payment method aamarpay :
| Action               | Endpoint                                                                       |
|----------------------|--------------------------------------------------------------------------------|
| Payment api-1        | [`/api`](https://school-management-five-iota.vercel.app/payment/api/) |
| Payment api-2        | [`/api2`](https://school-management-five-iota.vercel.app/payment/api2/) |
| Payment success        | [`/success`](https://school-management-five-iota.vercel.app/payment/success/) |
| Payment fail        | [`/fail`](https://school-management-five-iota.vercel.app/payment/fail/) |
| Payment cancel        | [`/cancel`](https://school-management-five-iota.vercel.app/payment/cancel/) |


---


### Setup
```bash
# Clone the repository
git clone https://github.com/Md-Merazul-Islam/School-Management-Front-End.git
cd School-Management-Front-End


# Start t
py manage.py runserver
