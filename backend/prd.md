# EcoSphere: ESG Management Platform - Backend PRD

## 1. Document Purpose
This document defines the backend product requirements for EcoSphere, an ESG Management Platform built with **MongoDB** and **Express.js**. It is written from the backend implementation perspective so engineering can design the API, data model, workflows, permissions, background jobs, calculations, and integrations required to support the frontend and reporting needs.

The backend is the system of record for all ESG master data, transactions, workflow state, scoring, notifications, and report generation.

## 2. Product Summary
EcoSphere helps organizations measure and improve Environmental, Social, and Governance performance directly from operational and workforce activity.

The backend must support:
- ESG master data setup
- Operational carbon calculations
- CSR and challenge participation workflows
- Governance audits and compliance issue tracking
- Gamification rules such as XP, badges, rewards, and leaderboards
- Configurable notification delivery
- Report generation and export
- Department and organization score aggregation
- Settings that control business rules such as auto-emission calculation, evidence enforcement, and badge auto-award

## 3. Goals
### Business Goals
- Centralize ESG data in a single backend platform.
- Replace manual ESG tracking with automated workflows.
- Provide reliable calculations for environmental, social, and governance scores.
- Support employee engagement through gamification.
- Enable reporting and compliance monitoring for management.

### Technical Goals
- Use MongoDB as the primary database.
- Use Express.js as the backend framework.
- Provide a clean REST API for frontend and integrations.
- Support scalable background processing for calculations, reminders, and report exports.
- Make ESG rules configurable per organization.
- Keep calculations auditable and traceable.

## 4. Scope
### In Scope
- Authentication and authorization
- Organization-level settings and configuration
- Master data management
- Transactional ESG workflows
- Carbon transaction ingestion and calculation
- CSR activity participation
- Challenge lifecycle and participation
- Policy acknowledgements
- Audits and compliance issues
- Rewards redemption
- Badges and leaderboard scoring
- Notifications
- Report generation and export
- Dashboard metrics and aggregation endpoints

### Out of Scope for Initial Release
- Native mobile app
- AI-based ESG recommendations
- External carbon registry settlement
- Blockchain verification
- Multi-tenant billing engine

## 5. Technology Stack
### Backend Stack
- Runtime: Node.js
- Framework: Express.js
- Database: MongoDB
- ORM/ODM: Mongoose or equivalent MongoDB ODM
- Authentication: JWT-based authentication with refresh token support
- File Storage: S3-compatible object storage or equivalent
- Background Jobs: BullMQ, Agenda, or equivalent queue/worker system
- Validation: Zod, Joi, or equivalent request validation library
- Logging: Structured logs with request correlation IDs
- API Style: REST

### Recommended Supporting Services
- Redis for job queues, rate limiting, and caching
- Object storage for proof files, audit attachments, and exported reports
- SMTP or email provider for notifications
- Optional PDF generation service for report exports

## 6. User Roles and Access Model
### Roles
- Super Admin: manages system-wide configuration and organization onboarding
- ESG Admin: manages ESG master data, settings, approvals, reports
- Department Head: views departmental scores, reviews activities, handles issues
- Manager: approves CSR and challenge submissions, tracks teams
- Employee: participates in CSR activities, challenges, policy acknowledgements, rewards redemption
- Auditor: manages audits, findings, and compliance issues
- Viewer: read-only dashboard and reporting access

### Access Principles
- Every record must be scoped to an organization.
- Department-based visibility should be supported for dashboards and reports.
- Approval actions must be permissioned by role.
- Sensitive records such as policy acknowledgements, audits, and compliance issues must be auditable.

## 7. Core Backend Modules

## 7.1 Authentication and Authorization
### Responsibilities
- Sign in and sign out
- Issue and refresh JWT tokens
- Role-based access control
- Optional department-based access restrictions
- Password reset and account recovery
- Session revocation and token rotation

### Requirements
- Secure password hashing
- Token expiration and refresh flow
- Middleware for role checks and feature checks
- Audit log for sign-in, approvals, redemptions, and administrative changes

## 7.2 Master Data Management
Master data must be configurable through backend APIs and used by transactional modules.

### Entities
- Department
- Category
- Emission Factor
- Product ESG Profile
- Environmental Goal
- ESG Policy
- Badge
- Reward
- Challenge template metadata if needed

### Requirements
- CRUD APIs for master records
- Validation of uniqueness where required
- Soft delete or status-based archival for controlled history
- Department hierarchy support with parent-child relationships
- Category types for CSR Activity and Challenge
- Status management for active/inactive records

## 7.3 Environmental Module
### Responsibilities
- Store carbon transactions
- Calculate emissions from operational data
- Map source records to emission factors
- Aggregate emissions by department, period, product, and category
- Track sustainability goals
- Produce environmental report datasets

### Carbon Transaction Sources
- Purchase
- Manufacturing
- Expenses
- Fleet
- Manual carbon entries when auto-calculation is disabled or unavailable

### Auto Emission Calculation
When enabled in settings:
- New linked operational records should trigger carbon transaction calculation automatically.
- The system must resolve the correct emission factor based on product, category, activity, vehicle, material, or configured mapping.
- Calculation results must be stored as immutable transaction records.
- Recalculation should create adjustment entries rather than overwrite historical data.

### Environmental Outputs
- Total emissions by department
- Emissions trend over time
- Emissions by source
- Emissions by product or operational category
- Sustainability goal progress

## 7.4 Social Module
### Responsibilities
- Manage CSR activities
- Track employee participation in CSR events
- Enforce proof upload when evidence is required
- Award points for approved participation
- Track diversity and engagement metrics
- Support training completion tracking if supplied from HR data

### CSR Participation Rules
- CSR activity can have category, date, location, owner, capacity, and approval flow.
- Employee participation records must store proof attachment, approval status, points earned, and completion date.
- If the evidence requirement setting is enabled, approval cannot be granted without proof.
- Participation approval should trigger notification events.

### Social Outputs
- Participation counts
- Approved vs pending participation
- CSR activity engagement by department
- Diversity and workforce participation indicators if available from source data

## 7.5 Governance Module
### Responsibilities
- Store ESG policies
- Capture policy acknowledgements
- Manage audits
- Track compliance issues with due dates and owners
- Trigger reminders and overdue notifications

### Policy Acknowledgements
- Employees must acknowledge assigned policies.
- The system must track acknowledgement date, policy version, and reminder status.
- Non-acknowledged policies should appear in dashboard metrics.

### Audits and Compliance Issues
- Each audit can generate one or more compliance issues.
- Every compliance issue must have an owner and due date.
- Open issues that pass the due date should be flagged as overdue.
- Overdue status should feed notifications and dashboards.

### Governance Outputs
- Open issues by severity
- Overdue compliance issue count
- Policy acknowledgement completion rate
- Audit completion status

## 7.6 Gamification Module
### Responsibilities
- Maintain challenge lifecycle
- Track challenge participation
- Calculate XP awards
- Manage badges and unlock rules
- Support reward redemption using XP or points
- Compute leaderboard rankings

### Challenge Lifecycle
- Draft
- Active
- Under Review
- Completed
- Archived

A challenge can be archived at any point. The backend must preserve historical participation records even when the challenge is archived.

### Challenge Participation
- Store progress percentage or milestone state
- Store proof files when evidence is required
- Store approval status and awarded XP
- Award XP only once per approved event unless defined otherwise

### Badge Auto-Award
When enabled:
- Badge assignment should happen automatically when an employee satisfies the unlock rule.
- Unlock rules may depend on XP, completed challenges, approved CSR activities, or other tracked metrics.
- Badge awards must be idempotent.
- Badge assignment should generate a notification.

### Reward Redemption
- Employees can redeem earned points or XP for rewards from the catalog.
- Redemption must validate stock availability.
- Redemption must deduct the required balance atomically.
- Redemption should be logged and reversible only through an admin process.

### Leaderboards
- Leaderboards should rank employees by XP, approved CSR participation, completed challenges, or a configurable blended score.
- Rankings should support filters by department and date range.

## 7.7 Scoring Engine
### Department Score
Each department receives:
- Environmental Score
- Social Score
- Governance Score
- Total Score

### Organization Score
The overall ESG score is a weighted average of department total scores. Default weights:
- Environmental: 40%
- Social: 30%
- Governance: 30%

Weights must be configurable per organization.

### Requirements
- Score calculations should be deterministic and traceable.
- Scores should be recalculated on a schedule and after important events.
- Historical snapshots must be preserved for reporting.
- Score components should expose the formulas and inputs used.

## 7.8 Notification System
### Notification Types
- Compliance issue created
- Compliance issue overdue
- CSR approval decision
- Challenge approval decision
- Policy acknowledgement reminder
- Badge unlocked
- Reward redemption outcome
- Goal milestone reached

### Delivery Channels
- In-app notifications
- Email notifications

### Requirements
- Notification preferences configurable in settings
- Event-driven notification creation
- Read/unread tracking
- Retry logic for failed email delivery
- Notification templates with localization-ready fields

## 7.9 Reporting Engine
### Required Reports
- Environmental Report
- Social Report
- Governance Report
- ESG Summary Report
- Custom Report Builder exports

### Report Filters
- Department
- Date Range
- Module
- Employee
- Challenge
- ESG Category

### Export Formats
- PDF
- Excel
- CSV

### Requirements
- Reports must use server-side aggregation.
- Export jobs should run asynchronously for heavy datasets.
- Generated files should be stored temporarily and downloadable via secure link.
- Reports should support repeatable queries and saved report definitions where needed.

## 8. Suggested MongoDB Data Model
The following collections are recommended.

### Master Collections
- departments
- categories
- emission_factors
- product_esg_profiles
- environmental_goals
- esg_policies
- badges
- rewards
- organization_settings
- notification_settings

### Transactional Collections
- carbon_transactions
- csr_activities
- employee_participations
- challenges
- challenge_participations
- policy_acknowledgements
- audits
- compliance_issues
- department_scores
- organization_scores
- notifications
- reward_redemptions
- audit_logs
- report_jobs
- leaderboard_snapshots

### Design Notes
- Use organizationId on every collection.
- Use departmentId where departmental filtering is needed.
- Keep history immutable for score snapshots, carbon transactions, awards, and redemptions.
- Use indexes for date, organization, department, employee, status, and due date fields.
- Store file metadata separately from binary storage references.

### Shared Document Fields
Most collections should include these standard fields where applicable:
- _id
- organizationId
- createdBy
- updatedBy
- createdAt
- updatedAt
- status
- notes
- attachments

### Collection Schemas
#### departments
- code
- name
- parentDepartmentId
- headUserId
- employeeCount
- status

#### categories
- name
- type
- description
- color
- status

#### emission_factors
- name
- sourceType
- unit
- factorValue
- validFrom
- validTo
- status
- metadata

#### product_esg_profiles
- productId
- productName
- categoryId
- emissionFactorId
- packagingType
- recyclable
- sustainabilityAttributes
- status

#### environmental_goals
- title
- description
- metricType
- targetValue
- unit
- startDate
- endDate
- ownerDepartmentId
- progressValue
- status

#### esg_policies
- title
- policyCode
- version
- category
- effectiveDate
- expiryDate
- documentUrl
- acknowledgementRequired
- status

#### badges
- name
- description
- icon
- unlockRuleType
- unlockRuleValue
- unlockRuleJson
- xpThreshold
- completedChallengesThreshold
- status

#### rewards
- name
- description
- pointsRequired
- xpRequired
- stock
- imageUrl
- redemptionLimitPerEmployee
- status

#### organization_settings
- organizationName
- scoringWeights
- autoEmissionCalculationEnabled
- evidenceRequirementEnabled
- badgeAutoAwardEnabled
- defaultCurrency
- locale
- timezone

#### notification_settings
- inAppEnabled
- emailEnabled
- reminderSchedule
- badgeUnlockNotifications
- complianceNotifications
- approvalNotifications
- policyReminderNotifications

#### carbon_transactions
- transactionType
- sourceModule
- sourceRecordId
- sourceRecordType
- departmentId
- employeeId
- productId
- emissionFactorId
- quantity
- unit
- emissionValue
- calculatedAt
- calculationMethod
- adjustmentOfTransactionId
- status

#### csr_activities
- title
- categoryId
- description
- location
- activityDate
- ownerUserId
- capacity
- evidenceRequired
- status

#### employee_participations
- employeeId
- csrActivityId
- proofFiles
- approvalStatus
- pointsEarned
- approvedBy
- approvedAt
- completionDate

#### challenges
- title
- categoryId
- description
- xpReward
- difficulty
- evidenceRequired
- deadline
- lifecycleStatus
- archivedAt
- ownerUserId

#### challenge_participations
- challengeId
- employeeId
- progress
- proofFiles
- approvalStatus
- xpAwarded
- approvedBy
- approvedAt
- completionDate

#### policy_acknowledgements
- policyId
- employeeId
- acknowledgedAt
- policyVersion
- reminderCount
- lastReminderAt
- status

#### audits
- title
- auditType
- startDate
- endDate
- auditorUserId
- departmentId
- status
- findingsSummary

#### compliance_issues
- auditId
- title
- severity
- description
- ownerUserId
- dueDate
- status
- overdueFlag
- resolvedAt
- resolutionNotes

#### department_scores
- departmentId
- environmentalScore
- socialScore
- governanceScore
- totalScore
- scoreDate
- scorePeriod

#### organization_scores
- environmentalWeight
- socialWeight
- governanceWeight
- environmentalScore
- socialScore
- governanceScore
- totalScore
- scoreDate

#### notifications
- recipientUserId
- type
- title
- message
- entityType
- entityId
- channel
- readAt
- sentAt
- deliveryStatus

#### reward_redemptions
- rewardId
- employeeId
- pointsSpent
- quantity
- redemptionCode
- status
- redeemedAt
- fulfilledAt

#### audit_logs
- actorUserId
- action
- entityType
- entityId
- payload
- ipAddress
- userAgent
- createdAt

#### report_jobs
- reportType
- filters
- requestedBy
- exportFormat
- fileUrl
- jobStatus
- startedAt
- completedAt

#### leaderboard_snapshots
- leaderboardType
- departmentId
- employeeId
- rank
- score
- xp
- snapshotDate
- period

## 9. Key API Groups
### Master Data APIs
- Department CRUD
- Category CRUD
- Emission Factor CRUD
- Product ESG Profile CRUD
- Goal CRUD
- Policy CRUD
- Badge CRUD
- Reward CRUD

### Operational APIs
- Carbon transaction ingestion
- CSR activity management
- Challenge lifecycle management
- Participation submission and approval
- Policy acknowledgement submission
- Audit creation and closure
- Compliance issue tracking
- Reward redemption

### Reporting APIs
- Dashboard summary
- Department scores
- Environmental/social/governance report data
- ESG summary report data
- Custom report builder preview and export

### System APIs
- Authentication
- User profile
- Notification preferences
- Notification inbox
- Background job status
- Settings management

## 9.1 REST API Route Catalog
Base path: /api/v1

### Authentication
- POST /auth/login
- POST /auth/logout
- POST /auth/refresh
- POST /auth/forgot-password
- POST /auth/reset-password
- GET /auth/me

### Users and Access
- GET /users
- POST /users
- GET /users/:id
- PATCH /users/:id
- DELETE /users/:id
- GET /roles
- POST /roles
- GET /permissions

### Organizations and Settings
- GET /organizations/:id/settings
- PATCH /organizations/:id/settings
- GET /notification-settings
- PATCH /notification-settings
- GET /esg-settings
- PATCH /esg-settings

### Departments
- GET /departments
- POST /departments
- GET /departments/:id
- PATCH /departments/:id
- DELETE /departments/:id
- GET /departments/:id/tree
- GET /departments/:id/scores

### Categories
- GET /categories
- POST /categories
- GET /categories/:id
- PATCH /categories/:id
- DELETE /categories/:id

### Emission Factors
- GET /emission-factors
- POST /emission-factors
- GET /emission-factors/:id
- PATCH /emission-factors/:id
- DELETE /emission-factors/:id

### Product ESG Profiles
- GET /product-esg-profiles
- POST /product-esg-profiles
- GET /product-esg-profiles/:id
- PATCH /product-esg-profiles/:id
- DELETE /product-esg-profiles/:id

### Environmental Goals
- GET /goals
- POST /goals
- GET /goals/:id
- PATCH /goals/:id
- DELETE /goals/:id

### ESG Policies
- GET /policies
- POST /policies
- GET /policies/:id
- PATCH /policies/:id
- DELETE /policies/:id

### Carbon Transactions
- GET /carbon-transactions
- POST /carbon-transactions
- GET /carbon-transactions/:id
- PATCH /carbon-transactions/:id
- DELETE /carbon-transactions/:id
- POST /carbon-transactions/calculate
- POST /carbon-transactions/recalculate

### CSR Activities and Participation
- GET /csr-activities
- POST /csr-activities
- GET /csr-activities/:id
- PATCH /csr-activities/:id
- DELETE /csr-activities/:id
- POST /csr-activities/:id/participations
- GET /csr-activities/:id/participations
- PATCH /participations/:id/approve
- PATCH /participations/:id/reject

### Challenges and Challenge Participation
- GET /challenges
- POST /challenges
- GET /challenges/:id
- PATCH /challenges/:id
- DELETE /challenges/:id
- PATCH /challenges/:id/archive
- PATCH /challenges/:id/activate
- POST /challenges/:id/participations
- GET /challenges/:id/participations
- PATCH /challenge-participations/:id/approve
- PATCH /challenge-participations/:id/reject

### Policy Acknowledgements
- GET /policy-acknowledgements
- POST /policy-acknowledgements
- GET /policy-acknowledgements/:id
- PATCH /policy-acknowledgements/:id/remind

### Audits and Compliance
- GET /audits
- POST /audits
- GET /audits/:id
- PATCH /audits/:id
- DELETE /audits/:id
- GET /compliance-issues
- POST /compliance-issues
- GET /compliance-issues/:id
- PATCH /compliance-issues/:id
- PATCH /compliance-issues/:id/resolve
- PATCH /compliance-issues/:id/reopen

### Badges, Rewards, and Leaderboards
- GET /badges
- POST /badges
- GET /badges/:id
- PATCH /badges/:id
- DELETE /badges/:id
- GET /rewards
- POST /rewards
- GET /rewards/:id
- PATCH /rewards/:id
- DELETE /rewards/:id
- POST /rewards/:id/redeem
- GET /leaderboards
- GET /leaderboards/department/:departmentId

### Notifications
- GET /notifications
- GET /notifications/:id
- PATCH /notifications/:id/read
- PATCH /notifications/read-all

### Reports and Dashboards
- GET /dashboard/summary
- GET /dashboard/environmental
- GET /dashboard/social
- GET /dashboard/governance
- GET /reports/environmental
- GET /reports/social
- GET /reports/governance
- GET /reports/summary
- POST /reports/custom/preview
- POST /reports/custom/export
- GET /reports/jobs
- GET /reports/jobs/:id

### Audit and System Utilities
- GET /audit-logs
- GET /health
- GET /jobs/:id

## 9.2 Query, Filter, and Payload Conventions
### List Endpoints
- Support `page`, `limit`, `sortBy`, and `sortOrder` on all list endpoints.
- Support `search` for keyword lookup where relevant.
- Support `departmentId`, `employeeId`, `categoryId`, `status`, `startDate`, and `endDate` filters when applicable.
- Return pagination metadata with `total`, `page`, `limit`, and `totalPages`.

### Standard Response Shape
- success
- message
- data
- meta
- errors

### Standard Error Shape
- code
- message
- details
- fieldErrors

### File Upload Rules
- Accept proof files, policy attachments, badge icons, reward images, and export files.
- Validate MIME type and file size before upload.
- Store metadata in MongoDB and binary content in object storage.
- Return a durable file reference id and a secure download URL when permitted.

## 9.3 Route Input and Response Matrix
All list endpoints return:
- data: array of records
- meta: page, limit, total, totalPages

All create/update endpoints return:
- data: the created or updated record

All detail endpoints return:
- data: the requested record with related summary fields where useful

### Authentication
- POST /auth/login
	- Input: email, password
	- Response: accessToken, refreshToken, user, role, organization
- POST /auth/logout
	- Input: refreshToken or session id
	- Response: success message
- POST /auth/refresh
	- Input: refreshToken
	- Response: new accessToken and refreshToken
- POST /auth/forgot-password
	- Input: email
	- Response: reset request accepted
- POST /auth/reset-password
	- Input: token, newPassword
	- Response: password reset success
- GET /auth/me
	- Input: auth header only
	- Response: current user profile, permissions, organization, settings flags

### Users and Roles
- GET /users
	- Input: page, limit, search, role, departmentId, status
	- Response: paginated users with department and role summary
- POST /users
	- Input: name, email, password, roleIds, departmentId, status
	- Response: created user record
- GET /users/:id
	- Input: user id in path
	- Response: user record with role list and department info
- PATCH /users/:id
	- Input: editable user fields, roleIds, departmentId, status
	- Response: updated user record
- DELETE /users/:id
	- Input: user id in path
	- Response: soft delete success message
- GET /roles
	- Input: page, limit, search
	- Response: paginated role list
- POST /roles
	- Input: name, permissions, status
	- Response: created role

### Organization Settings
- GET /organizations/:id/settings
	- Input: organization id in path
	- Response: scoring weights, feature toggles, notification flags, timezone, currency
- PATCH /organizations/:id/settings
	- Input: scoringWeights, autoEmissionCalculationEnabled, evidenceRequirementEnabled, badgeAutoAwardEnabled, notification flags
	- Response: updated settings record
- GET /notification-settings
	- Input: auth context
	- Response: notification channels, reminder timing, toggle states
- PATCH /notification-settings
	- Input: inAppEnabled, emailEnabled, reminderSchedule, notification toggle flags
	- Response: updated notification settings

### Departments
- GET /departments
	- Input: page, limit, search, status, parentDepartmentId
	- Response: department list with employeeCount and head summary
- POST /departments
	- Input: name, code, headUserId, parentDepartmentId, status
	- Response: created department
- GET /departments/:id
	- Input: department id
	- Response: department detail, hierarchy summary, employeeCount
- PATCH /departments/:id
	- Input: name, code, headUserId, parentDepartmentId, status
	- Response: updated department
- GET /departments/:id/tree
	- Input: department id
	- Response: nested child departments
- GET /departments/:id/scores
	- Input: department id, periodStart, periodEnd
	- Response: environmental, social, governance, total score

### Categories, Emission Factors, Products, Goals, Policies
- GET /categories, /emission-factors, /product-esg-profiles, /goals, /policies
	- Input: page, limit, search, status, type, categoryId as relevant
	- Response: paginated master data list
- POST /categories
	- Input: name, type, description, status
	- Response: created category
- POST /emission-factors
	- Input: name, sourceType, unit, factorValue, validFrom, validTo, status, metadata
	- Response: created emission factor
- POST /product-esg-profiles
	- Input: productId, productName, categoryId, emissionFactorId, sustainabilityAttributes, status
	- Response: created product ESG profile
- POST /goals
	- Input: title, metricType, targetValue, unit, startDate, endDate, ownerDepartmentId, status
	- Response: created goal
- POST /policies
	- Input: title, policyCode, version, content or documentUrl, acknowledgementRequired, status
	- Response: created policy

### Carbon Transactions
- GET /carbon-transactions
	- Input: page, limit, departmentId, employeeId, productId, sourceType, startDate, endDate
	- Response: carbon transaction list with emissionValue and source summary
- POST /carbon-transactions
	- Input: sourceType, sourceRecordId, departmentId, employeeId, productId, emissionFactorId, quantity, unit, calculationMethod
	- Response: created carbon transaction and calculated emissionValue
- POST /carbon-transactions/calculate
	- Input: source record reference or batch of source records
	- Response: created carbon transaction records and calculation summary
- PATCH /carbon-transactions/:id
	- Input: editable manual fields, remarks, adjustmentOfTransactionId when needed
	- Response: updated transaction or adjustment record

### CSR Activities and Participation
- POST /csr-activities
	- Input: title, categoryId, description, location, activityDate, ownerUserId, capacity, pointsEarned, evidenceRequired, status
	- Response: created CSR activity
- GET /csr-activities
	- Input: page, limit, search, categoryId, status, startDate, endDate
	- Response: activity list with participation counts
- POST /csr-activities/:id/participations
	- Input: employeeId, proofFiles, remarks
	- Response: participation record with pending approval status
- PATCH /participations/:id/approve
	- Input: approval remarks
	- Response: approved participation, points earned, notification result
- PATCH /participations/:id/reject
	- Input: rejection remarks
	- Response: rejected participation

### Challenges and Challenge Participation
- POST /challenges
	- Input: title, categoryId, description, xp, difficulty, evidenceRequired, deadline, startDate, status
	- Response: created challenge
- GET /challenges
	- Input: page, limit, search, categoryId, status, startDate, endDate
	- Response: challenge list with participant and status summary
- POST /challenges/:id/participations
	- Input: employeeId, progress, proofFiles, remarks
	- Response: participation record with pending approval status
- PATCH /challenge-participations/:id/approve
	- Input: xpAwarded, approval remarks
	- Response: approved participation, XP update, badge check result
- PATCH /challenge-participations/:id/reject
	- Input: rejection remarks
	- Response: rejected participation

### Policy Acknowledgements
- POST /policy-acknowledgements
	- Input: policyId, employeeId, policyVersion, acknowledgementDate
	- Response: acknowledgement record
- GET /policy-acknowledgements
	- Input: page, limit, employeeId, policyId, status
	- Response: acknowledgement list with reminder status
- PATCH /policy-acknowledgements/:id/remind
	- Input: reminder note or scheduled reminder flag
	- Response: reminder sent status

### Audits and Compliance
- POST /audits
	- Input: title, auditType, departmentId, ownerUserId, startDate, endDate, status
	- Response: created audit record
- GET /audits
	- Input: page, limit, departmentId, status, startDate, endDate
	- Response: audit list with issue count
- POST /compliance-issues
	- Input: auditId, title, severity, description, ownerUserId, dueDate, status
	- Response: created compliance issue
- PATCH /compliance-issues/:id
	- Input: title, severity, description, ownerUserId, dueDate, status, resolutionNotes
	- Response: updated issue
- PATCH /compliance-issues/:id/resolve
	- Input: resolutionNotes
	- Response: resolved issue

### Badges, Rewards, and Leaderboards
- POST /badges
	- Input: name, description, icon, unlockRuleType, unlockRuleValue, unlockRuleJson, status
	- Response: created badge
- GET /badges
	- Input: page, limit, search, status
	- Response: badge list with unlock rule summary
- POST /rewards
	- Input: name, description, pointsRequired, xpRequired, stock, imageUrl, redemptionLimitPerEmployee, status
	- Response: created reward
- POST /rewards/:id/redeem
	- Input: employeeId, quantity
	- Response: redemption record, remaining balance, remaining stock
- GET /leaderboards
	- Input: leaderboardType, departmentId, startDate, endDate, limit
	- Response: ranked list with score, xp, and badge summary

### Notifications, Reports, Jobs
- GET /notifications
	- Input: page, limit, isRead, type
	- Response: notification list
- PATCH /notifications/:id/read
	- Input: none
	- Response: read status updated
- GET /dashboard/summary
	- Input: departmentId, startDate, endDate
	- Response: ESG totals, pending actions, and trend cards
- POST /reports/custom/preview
	- Input: reportType, filters, columns, dateRange, departmentId, employeeId, challengeId, exportFormat
	- Response: preview rows and summary totals
- POST /reports/custom/export
	- Input: reportType, filters, exportFormat
	- Response: report job record and download link when complete
- GET /reports/jobs/:id
	- Input: report job id
	- Response: job status, progress, and fileUrl if ready

## 9.4 Workflow State Machines
### CSR Activity Participation
- Draft
- Submitted
- Pending Approval
- Approved
- Rejected
- Cancelled

### Challenge Lifecycle
- Draft
- Active
- Under Review
- Completed
- Archived

### Challenge Participation
- Draft
- Submitted
- Pending Approval
- Approved
- Rejected

### Policy Acknowledgement
- Pending
- Acknowledged
- Overdue

### Audit
- Open
- In Progress
- Closed
- Archived

### Compliance Issue
- Open
- In Review
- Resolved
- Closed
- Overdue

### Reward Redemption
- Pending
- Approved
- Fulfilled
- Cancelled
- Rejected

### Report Job
- Queued
- Running
- Completed
- Failed

## 9.5 Event and Automation Matrix
The backend should emit internal events or queue jobs for these actions.

### Core Events
- auth.user.logged_in
- settings.updated
- carbon.transaction.created
- carbon.transaction.recalculated
- csr.participation.submitted
- csr.participation.approved
- csr.participation.rejected
- challenge.created
- challenge.published
- challenge.participation.submitted
- challenge.participation.approved
- challenge.participation.rejected
- policy.acknowledged
- audit.created
- compliance.issue.created
- compliance.issue.overdue
- reward.redeemed
- badge.unlocked
- score.recalculated
- report.job.created
- report.job.completed

### Automated Jobs
- Daily score recalculation
- Overdue compliance checker
- Policy acknowledgement reminder sender
- Notification delivery worker
- Badge auto-award evaluator
- Carbon transaction calculation worker
- Report export worker
- Reward stock reconciliation worker

## 9.6 Calculation Rules and Business Logic
### Carbon Calculation
- emissionValue = quantity x emissionFactor.factorValue
- If a unit conversion is required, convert before the multiplication step.
- Adjustments must be stored as separate records, not direct mutations.

### Department Score
- Department score should aggregate the latest approved and calculated metrics for the configured period.
- Environmental, social, and governance components should remain independently queryable.

### Organization Score
- totalScore = (environmentalScore x envWeight) + (socialScore x socialWeight) + (governanceScore x govWeight)
- Weights must sum to 1 or 100, depending on implementation choice, and must be normalized consistently.

### Badge Auto-Award
- The evaluator should run after XP-changing or progress-changing events.
- A badge may only be granted once per employee unless the badge definition explicitly allows repeat awards.

### Reward Redemption
- Validate employee balance, reward stock, and redemption rules in one atomic transaction.
- If any validation fails, the redemption must rollback completely.

### Compliance Overdue Detection
- Any open issue with dueDate < currentDate becomes overdue.
- Overdue issues should trigger notifications and appear in dashboard counters.

## 9.7 API Security and Governance
### Authentication
- JWT access tokens for API access.
- Refresh tokens for session renewal.
- Token revocation on logout or account disable.

### Authorization
- Role-based access control on every sensitive route.
- Department-scoped access where required.
- Admin-only access for settings, master data, and override actions.

### Auditability
- Log all create, update, delete, approve, reject, redeem, and export actions.
- Store actor, timestamp, entity id, and before/after snapshots where relevant.

### Rate Limiting and Safety
- Protect auth and export endpoints with rate limits.
- Validate all incoming payloads.
- Reject unknown fields when practical to avoid silent schema drift.

## 9.8 Non-Functional Requirements
### Performance
- Dashboard summary endpoints should complete quickly for a typical organization.
- Heavy filters and exports should use aggregation pipelines and async jobs.
- Indexes must exist for all common query paths.

### Reliability
- Background jobs must retry on transient failure.
- Notification delivery and report exports need job state tracking.
- Partial failures should not corrupt reward, score, or carbon history.

### Observability
- Structured logs with correlation ids.
- Health and metrics endpoints.
- Error tracking for background jobs and failed deliveries.

### Scalability
- The design should support growth in employees, transactions, and reports without changing the core schema model.

## 9.9 Implementation Phases
### Phase 1
- Auth, RBAC, settings, departments, categories, emission factors, ESG policies, basic dashboard, carbon transactions, CSR, and challenges.

### Phase 2
- Approvals, policy acknowledgements, compliance issues, audits, notifications, rewards, badges, and leaderboards.

### Phase 3
- Reports, exports, advanced analytics, score history, and scheduled automation.

### Phase 4
- Hardening, observability, tuning, and production readiness.

## 9.10 Backend Acceptance Criteria
The backend PRD is complete when:
- Every business module has a corresponding MongoDB collection or derived aggregation.
- Every major flow has a route in the REST API catalog.
- ESG calculations, rewards, approvals, notifications, and reports are deterministic and traceable.
- Required validations are enforced by the backend, not the frontend.
- Settings toggles change system behavior without code changes.
- The data model supports organization-wide and department-level reporting.
- Exported reports and notifications can be generated asynchronously.
- Historical records remain immutable where required for audit and compliance.

## 10. Validation and Business Rules
### Required Rules
- Compliance Issue must have Owner and Due Date.
- Open Compliance Issues past due date must be flagged overdue.
- Reward redemption must fail if balance is insufficient or stock is unavailable.
- If evidence requirement is enabled, CSR approval requires proof.
- Badge auto-award must be idempotent.
- Auto-emission calculation must only run when enabled.
- Department score calculations must be reproducible.
- Challenge archival must not delete historical participation.

### Recommended Rules
- Prevent duplicate acknowledgements for the same policy version.
- Prevent duplicate approval transitions.
- Prevent double spending of reward points.
- Enforce status transitions for challenge lifecycle.

## 11. Non-Functional Requirements
### Performance
- Common dashboard endpoints should respond quickly under normal organization scale.
- Heavy report exports should be asynchronous.
- Indexes must support reporting filters and department drill-down.

### Reliability
- Background jobs must be retryable.
- Failed notification sends must be tracked.
- Export jobs should be recoverable after interruption.

### Security
- JWT authentication
- Role-based access control
- File upload validation
- Input validation on all endpoints
- Audit logs for sensitive operations
- Secure storage for attachments and exports

### Observability
- Structured logs
- Request tracing
- Job monitoring
- Error reporting
- Metrics for notification delivery and report generation

## 12. Backend Implementation Priorities
### Phase 1
- Authentication and organization setup
- Master data CRUD
- ESG settings
- Carbon transaction storage
- CSR activity and challenge data models
- Policy acknowledgement flow

### Phase 2
- Approval workflows
- Notification engine
- Reward redemption
- Badge auto-award
- Department score aggregation

### Phase 3
- Report builder
- Export pipelines
- Advanced dashboards
- Scheduled recalculations
- Leaderboards and historical analytics

## 13. Acceptance Criteria
The backend is considered ready when:
- All master and transactional modules can be created, read, updated, and reported through APIs.
- MongoDB stores the full ESG domain model with organization scoping.
- Express APIs enforce the stated business rules.
- Notifications are emitted for the required events.
- Reward redemption is transactional and stock-aware.
- Score aggregation and reports work with the specified filters.
- Auto-emission calculation, evidence enforcement, and badge auto-award are configurable and functional.
- Compliance issues support owner, due date, and overdue detection.

## 14. Open Implementation Notes
- Finalize whether Mongoose or a lighter MongoDB driver abstraction will be used.
- Confirm whether PDF export is generated in-process or by a worker service.
- Confirm whether notifications require SMS or only in-app/email for the first release.
- Confirm whether employee profile data is sourced from an external HR system or managed locally.
