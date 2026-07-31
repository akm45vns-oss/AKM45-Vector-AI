"""Initial schema migration: users, companies, jobs, skills, resumes, applications

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-07-31

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enum types
    user_role_enum = postgresql.ENUM('admin', 'recruiter', 'candidate', name='userrole')
    user_role_enum.create(op.get_bind(), checkfirst=True)

    job_status_enum = postgresql.ENUM('draft', 'published', 'closed', 'archived', name='jobstatus')
    job_status_enum.create(op.get_bind(), checkfirst=True)

    employment_type_enum = postgresql.ENUM('full_time', 'part_time', 'contract', 'remote', 'internship', name='employmenttype')
    employment_type_enum.create(op.get_bind(), checkfirst=True)

    app_status_enum = postgresql.ENUM('applied', 'screening', 'shortlisted', 'interviewing', 'offered', 'rejected', 'withdrawn', name='applicationstatus')
    app_status_enum.create(op.get_bind(), checkfirst=True)

    # 1. users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'recruiter', 'candidate', name='userrole'), nullable=False, server_default='candidate'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_email_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('email_verification_token', sa.String(length=255), nullable=True),
        sa.Column('password_reset_token', sa.String(length=255), nullable=True),
        sa.Column('password_reset_expires', sa.DateTime(timezone=True), nullable=True),
        sa.Column('avatar_url', sa.String(length=512), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_role', 'users', ['role'])

    # 2. companies table
    op.create_table(
        'companies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('website', sa.String(length=512), nullable=True),
        sa.Column('industry', sa.String(length=120), nullable=True),
        sa.Column('size', sa.String(length=50), nullable=True),
        sa.Column('logo_url', sa.String(length=512), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_by_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_companies_id', 'companies', ['id'])
    op.create_index('ix_companies_name', 'companies', ['name'])
    op.create_index('ix_companies_industry', 'companies', ['industry'])

    # 3. jobs table
    op.create_table(
        'jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False),
        sa.Column('recruiter_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('requirements', sa.Text(), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('employment_type', sa.Enum('full_time', 'part_time', 'contract', 'remote', 'internship', name='employmenttype'), nullable=False, server_default='full_time'),
        sa.Column('status', sa.Enum('draft', 'published', 'closed', 'archived', name='jobstatus'), nullable=False, server_default='draft'),
        sa.Column('min_salary', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('max_salary', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('currency', sa.String(length=3), server_default='USD', nullable=False),
        sa.Column('experience_years_required', sa.Integer(), server_default='0', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_jobs_id', 'jobs', ['id'])
    op.create_index('ix_jobs_company_id', 'jobs', ['company_id'])
    op.create_index('ix_jobs_recruiter_id', 'jobs', ['recruiter_id'])
    op.create_index('ix_jobs_title', 'jobs', ['title'])
    op.create_index('ix_jobs_status', 'jobs', ['status'])
    op.create_index('ix_jobs_location', 'jobs', ['location'])

    # 4. skills table
    op.create_table(
        'skills',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
    )
    op.create_index('ix_skills_id', 'skills', ['id'])
    op.create_index('ix_skills_name', 'skills', ['name'], unique=True)
    op.create_index('ix_skills_category', 'skills', ['category'])

    # 5. resumes table
    op.create_table(
        'resumes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('file_path', sa.String(length=512), nullable=False),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=False),
        sa.Column('raw_text', sa.Text(), nullable=True),
        sa.Column('parsed_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('embedding', postgresql.ARRAY(sa.Float()), nullable=True),
        sa.Column('ats_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_resumes_id', 'resumes', ['id'])
    op.create_index('ix_resumes_user_id', 'resumes', ['user_id'])

    # 6. resume_skills table
    op.create_table(
        'resume_skills',
        sa.Column('resume_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('resumes.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('years_experience', sa.Float(), nullable=True),
        sa.Column('proficiency_level', sa.String(length=50), nullable=True),
    )

    # 7. job_skills table
    op.create_table(
        'job_skills',
        sa.Column('job_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('jobs.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('skill_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('is_required', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('weight', sa.Float(), server_default='1.0', nullable=False),
    )

    # 8. applications table
    op.create_table(
        'applications',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('job_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('resume_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('status', sa.Enum('applied', 'screening', 'shortlisted', 'interviewing', 'offered', 'rejected', 'withdrawn', name='applicationstatus'), nullable=False, server_default='applied'),
        sa.Column('match_score', sa.Float(), nullable=True),
        sa.Column('match_breakdown', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('llm_feedback', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('applied_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_applications_id', 'applications', ['id'])
    op.create_index('ix_applications_job_id', 'applications', ['job_id'])
    op.create_index('ix_applications_resume_id', 'applications', ['resume_id'])
    op.create_index('ix_applications_candidate_id', 'applications', ['candidate_id'])
    op.create_index('ix_applications_status', 'applications', ['status'])


def downgrade() -> None:
    op.drop_table('applications')
    op.drop_table('job_skills')
    op.drop_table('resume_skills')
    op.drop_table('resumes')
    op.drop_table('skills')
    op.drop_table('jobs')
    op.drop_table('companies')
    op.drop_table('users')

    op.execute('DROP TYPE IF EXISTS applicationstatus')
    op.execute('DROP TYPE IF EXISTS employmenttype')
    op.execute('DROP TYPE IF EXISTS jobstatus')
    op.execute('DROP TYPE IF EXISTS userrole')
