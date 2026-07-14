from enum import Enum
from typing import Set, Dict, List
from loguru import logger

class Role(str, Enum):
    """User roles in the system"""
    ADMIN = "admin"
    USER = "user"
    TEACHER = "teacher"
    PARENT = "parent"
    STUDENT = "student"

class Permission(str, Enum):
    """System permissions"""
    # User management
    CREATE_USER = "create_user"
    READ_USER = "read_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    
    # Content management
    UPLOAD_DOCUMENT = "upload_document"
    DELETE_DOCUMENT = "delete_document"
    READ_DOCUMENT = "read_document"
    
    # AI features
    USE_AI_CHAT = "use_ai_chat"
    USE_VISION_AI = "use_vision_ai"
    USE_AGENTS = "use_agents"
    
    # Admin features
    MANAGE_SUBSCRIPTIONS = "manage_subscriptions"
    MANAGE_USERS = "manage_users"
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_SYSTEM = "manage_system"
    
    # Teacher features
    CREATE_COURSE = "create_course"
    MANAGE_ASSIGNMENTS = "manage_assignments"
    VIEW_STUDENT_PROGRESS = "view_student_progress"
    
    # Parent features
    VIEW_CHILD_PROGRESS = "view_child_progress"
    MANAGE_CHILD_ACCOUNT = "manage_child_account"

# Role-Permission mapping
ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.ADMIN: {
        # User management
        Permission.CREATE_USER,
        Permission.READ_USER,
        Permission.UPDATE_USER,
        Permission.DELETE_USER,
        
        # Content management
        Permission.UPLOAD_DOCUMENT,
        Permission.DELETE_DOCUMENT,
        Permission.READ_DOCUMENT,
        
        # AI features
        Permission.USE_AI_CHAT,
        Permission.USE_VISION_AI,
        Permission.USE_AGENTS,
        
        # Admin features
        Permission.MANAGE_SUBSCRIPTIONS,
        Permission.MANAGE_USERS,
        Permission.VIEW_ANALYTICS,
        Permission.MANAGE_SYSTEM,
        
        # Teacher features
        Permission.CREATE_COURSE,
        Permission.MANAGE_ASSIGNMENTS,
        Permission.VIEW_STUDENT_PROGRESS,
        
        # Parent features
        Permission.VIEW_CHILD_PROGRESS,
        Permission.MANAGE_CHILD_ACCOUNT,
    },
    
    Role.USER: {
        # Content management
        Permission.UPLOAD_DOCUMENT,
        Permission.DELETE_DOCUMENT,
        Permission.READ_DOCUMENT,
        
        # AI features
        Permission.USE_AI_CHAT,
        Permission.USE_VISION_AI,
        Permission.USE_AGENTS,
    },
    
    Role.TEACHER: {
        # Content management
        Permission.UPLOAD_DOCUMENT,
        Permission.DELETE_DOCUMENT,
        Permission.READ_DOCUMENT,
        
        # AI features
        Permission.USE_AI_CHAT,
        Permission.USE_VISION_AI,
        Permission.USE_AGENTS,
        
        # Teacher features
        Permission.CREATE_COURSE,
        Permission.MANAGE_ASSIGNMENTS,
        Permission.VIEW_STUDENT_PROGRESS,
    },
    
    Role.PARENT: {
        # AI features
        Permission.USE_AI_CHAT,
        Permission.USE_VISION_AI,
        Permission.USE_AGENTS,
        
        # Parent features
        Permission.VIEW_CHILD_PROGRESS,
        Permission.MANAGE_CHILD_ACCOUNT,
    },
    
    Role.STUDENT: {
        # Content management
        Permission.UPLOAD_DOCUMENT,
        Permission.DELETE_DOCUMENT,
        Permission.READ_DOCUMENT,
        
        # AI features
        Permission.USE_AI_CHAT,
        Permission.USE_VISION_AI,
        Permission.USE_AGENTS,
    },
}

class RBACManager:
    """Role-Based Access Control Manager"""
    
    @staticmethod
    def has_permission(role: Role, permission: Permission) -> bool:
        """Check if a role has a specific permission"""
        if role not in ROLE_PERMISSIONS:
            logger.warning(f"Unknown role: {role}")
            return False
        
        return permission in ROLE_PERMISSIONS[role]
    
    @staticmethod
    def has_any_permission(role: Role, permissions: List[Permission]) -> bool:
        """Check if a role has any of the specified permissions"""
        if role not in ROLE_PERMISSIONS:
            return False
        
        return any(perm in ROLE_PERMISSIONS[role] for perm in permissions)
    
    @staticmethod
    def has_all_permissions(role: Role, permissions: List[Permission]) -> bool:
        """Check if a role has all of the specified permissions"""
        if role not in ROLE_PERMISSIONS:
            return False
        
        return all(perm in ROLE_PERMISSIONS[role] for perm in permissions)
    
    @staticmethod
    def get_permissions(role: Role) -> Set[Permission]:
        """Get all permissions for a role"""
        return ROLE_PERMISSIONS.get(role, set())
    
    @staticmethod
    def check_permission(role: Role, permission: Permission) -> bool:
        """Check permission and log if denied"""
        if RBACManager.has_permission(role, permission):
            return True
        
        logger.warning(f"Permission denied: {role} does not have {permission}")
        return False

def require_permission(permission: Permission):
    """Decorator to require a specific permission"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # In a real implementation, you would extract the user's role
            # from the request context and check permissions
            # For now, this is a placeholder
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def require_role(role: Role):
    """Decorator to require a specific role"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # In a real implementation, you would extract the user's role
            # from the request context and check if it matches
            # For now, this is a placeholder
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def require_any_role(*roles: Role):
    """Decorator to require any of the specified roles"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # In a real implementation, you would extract the user's role
            # from the request context and check if it matches any of the roles
            # For now, this is a placeholder
            return await func(*args, **kwargs)
        return wrapper
    return decorator
