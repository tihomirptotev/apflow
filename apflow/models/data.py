
# Units in the structure of the organization
UNIT_TYPES = [
    ('department', 'Department'),
    ('branch', 'Branch'),
    ('office', 'Office')
]

# Types of account payable documents
AP_DOCUMENT_TYPES = [
    ('invoice', 'Invoice'),
    ('business_trip_order', 'Business Trip Order'),
    ('offer', 'Offer'),
    ('contract', 'Contract'),
]


# AP documents approval level
AP_DOCUMENT_APPROVAL_LEVELS = [
    ('approved_in_advance', 'Approved in Advance'),
    ('level_bn', 'Approval by Branch Network'),
    ('level_acc', 'Approval by Accounting Department'),
    ('level_exec', 'Approval by Executive Director'),
]


# AP Workflow status codes
AP_WORKFLOW_STATUS_CODES = [
    ('draft', 'Draft - not sent to higher level for approval'),
    ('adv_approved', 'Approved in Advance'),
    ('pending_bna', 'Pending Branch Network Approval'),
    ('pending_acc', 'Pending Accounting Department Approval'),
    ('pending_exec', 'Pending Executive Director Approval'),
    ('approved_final', 'Approved by the Responsible Level'),
]
