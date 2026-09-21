# Software Engineering Documentation: AI-Powered Project Idea Generator

---

## 1. Problem Statement

Computer Science and Information Technology students often encounter significant friction when selecting suitable academic project topics for capstone courses, semester assignments, or thesis research. Common challenges include:

1. **Lack of Domain Guidance**: Difficulty identifying realistic project scopes aligned with modern industry trends (e.g. AI/ML, Cybersecurity, Cloud, DevOps).
2. **Skill Mismatch**: Selecting projects that are either overly trivial or excessively complex for their technical skill level.
3. **Ambiguous Roadmap**: Inability to decompose abstract ideas into concrete execution steps, technology choices, and future scopes.
4. **Faculty Evaluation Gap**: Inadequate documentation of project objectives and future scope during proposal defense.

The **AI-Powered Project Idea Generator** addresses these challenges by automating the generation of structured, skill-matched, and domain-tailored project blueprints.

---

## 2. Project Objectives

- **Intelligent Recommendation Engine**: Match candidate domain interests, technical skills, and difficulty constraints with structured academic project ideas.
- **Comprehensive Blueprints**: Provide every recommendation with technology stacks, estimated timeline, step-by-step implementation roadmaps, and future scope.
- **Persistence & Personalization**: Allow students to bookmark project concepts to a private saved library.
- **Admin Control & Analytics**: Enable faculty/administrators to manage project offerings, review usage metrics, and monitor high-demand technological domains.
- **CI/CD & Quality Assurance**: Implement test automation (Pytest) and pipeline deployment automation (Jenkins).

---

## 3. Requirements Specification

### 3.1 Functional Requirements

| ID | Module | Requirement Description | Priority |
| :--- | :--- | :--- | :--- |
| **FR-01** | User Interface | Responsive web interface with dark glassmorphism design, navigation bar, and toast alerts. | High |
| **FR-02** | Home Page | Display platform overview, total project statistics, core features, and CTA buttons. | High |
| **FR-03** | Generator Input | Collect Student Name, Domain, Skills, and Difficulty level inputs. | High |
| **FR-04** | Recommendation | Calculate match scores and output at least 5 structured project recommendations. | High |
| **FR-05** | Save Feature | Enable users to save project recommendations and view/delete them in `/saved`. | High |
| **FR-06** | Admin Login | Authenticate administrators via secure username/password credentials (`admin`/`admin123`). | High |
| **FR-07** | Admin CRUD | Allow admin to add, edit, and delete project entries in real time. | High |
| **FR-08** | Admin Analytics | Render total users, published projects, saved count, and domain usage statistics. | Medium |
| **FR-09** | Clipboard Export | Provide one-click copy summary for project specifications. | Low |

### 3.2 Non-Functional Requirements

- **Performance**: Recommendation generation executed in under 200 milliseconds.
- **Usability**: Intuitive single-page form input with clear error feedback and validation hints.
- **Reliability**: SQLite foreign key constraints enabled with zero data loss during deletion cascades.
- **Portability**: Containerized deployment capability and cross-platform compatibility (Windows/Linux/macOS).
- **Security**: Admin session control, SQL parameterized queries preventing SQL injection vulnerabilities.

---

## 4. Use Case Analysis

### 4.1 Actors
1. **Student / Guest User**: Searches for project recommendations, saves projects, copies project blueprints.
2. **Administrator (Faculty)**: Manages project database entries, monitors usage analytics.

### 4.2 Use Case Descriptions

```
+-----------------------------------------------------------------------+
|                       System Boundary: IdeaGen AI                     |
|                                                                       |
|   (Student) ---------> [ UC-1: Generate Project Ideas ]              |
|       |                                                               |
|       +--------------> [ UC-2: Save Project to Library ]              |
|       |                                                               |
|       +--------------> [ UC-3: View & Delete Saved Ideas ]            |
|                                                                       |
|   (Admin) -----------> [ UC-4: Admin Authentication ]                 |
|       |                                                               |
|       +--------------> [ UC-5: Add / Edit / Delete Projects ]         |
|       |                                                               |
|       +--------------> [ UC-6: View Analytics Dashboard ]             |
+-----------------------------------------------------------------------+
```

| Use Case ID | Name | Primary Actor | Description |
| :--- | :--- | :--- | :--- |
| **UC-1** | Generate Projects | Student | Input domain, skills, difficulty to view ranked project recommendations. |
| **UC-2** | Save Project | Student | Store chosen recommendation to user's saved library. |
| **UC-3** | Manage Saved | Student | View bookmarked projects and remove unwanted entries. |
| **UC-4** | Admin Login | Administrator | Authenticate into administrative portal. |
| **UC-5** | Project CRUD | Administrator | Add new project ideas or edit existing database records. |
| **UC-6** | View Analytics | Administrator | Inspect system metrics, generation counts, and domain demand. |

---

## 5. Risk Analysis & Mitigation Matrix

| Risk ID | Identified Risk | Impact | Probability | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **R-01** | Empty recommendation result set for obscure domain/skill queries. | High | Medium | Implement fallback algorithm ensuring at least 5 projects are returned across adjacent domains. |
| **R-02** | SQL Injection vulnerability via user input fields. | Critical | Low | Enforce parameterized queries (`sqlite3` bindings) across all database operations. |
| **R-03** | Database locking issues in concurrent SQLite environments. | Medium | Low | Use isolated connections with proper context manager closure per HTTP request. |
| **R-04** | CI/CD build failure during dependency installation. | High | Low | Pin exact package version numbers in `requirements.txt`. |

---

## 6. Software Testing Strategy

### 6.1 Testing Levels
1. **Unit Testing**: Testing individual database helper methods, recommendation scoring functions, and user creation.
2. **Integration Testing**: Verifying Flask route handling, request context processing, and SQLite persistence.
3. **End-to-End System Testing**: Executing simulated browser requests covering the full user flow: Form Submission -> Recommendation -> Save -> View Library -> Delete.
4. **CI/CD Automated Execution**: Running Pytest automatically in the Jenkins pipeline prior to build verification.

### 6.2 Test Matrix Summary

```text
============================= Test Matrix Results =============================
test_homepage_loading ................................................. PASSED
test_database_connection .............................................. PASSED
test_project_generation ............................................... PASSED
test_admin_login_success_and_failure .................................. PASSED
test_save_and_delete_project_feature .................................. PASSED
test_saved_projects_route ............................................. PASSED
============================== 6 Passed in 0.94s ==============================
```
