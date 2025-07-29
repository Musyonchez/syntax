# SyntaxMem - Development TODO List

**Simple, Uniform, Consistent** - Task tracking for current development cycle.

## 🧪 **Phase 1: Test Current Implementation**
- [ ] **Test login flow** - Verify Google OAuth + backend authentication
- [ ] **Test new user registration** - Ensure user creation works properly  
- [ ] **Test session persistence** - Check NextAuth session with backend data
- [ ] **Test dashboard access** - Verify protected route functionality
- [ ] **Test logout flow** - Confirm session cleanup works
- [ ] **Test token refresh** - Verify refresh token functionality (if implemented)

---

## 🔧 **Phase 2: Session Management Improvements**

### **Priority 1: Critical Database Hygiene**
- [ ] **Token cleanup (5 minutes)** - Critical database hygiene
  - [ ] Auto-cleanup expired refresh tokens from database
  - [ ] Optional: Remove old tokens on new login (prevent accumulation)
  - [ ] Add database indexes for efficient cleanup queries

### **Priority 2: Essential Security** 
- [ ] **"Log out all devices" (10 minutes)** - Essential security
  - [ ] Add `/logout-all` endpoint to revoke all user refresh tokens
  - [ ] Add "Sign out all devices" button to dashboard/profile
  - [ ] Update client to call logout-all endpoint

### **Priority 3: Simple Safeguard**
- [ ] **Optional session limit (5 minutes)** - Simple safeguard  
  - [ ] Limit users to reasonable number of concurrent sessions (5-10)
  - [ ] Remove oldest tokens when limit exceeded
  - [ ] Add configuration for session limit

---

## 🎯 **Phase 3: Testing & Validation**
- [ ] **Test token cleanup** - Verify expired tokens are removed
- [ ] **Test "log out all devices"** - Confirm all sessions invalidated
- [ ] **Test session limits** - Ensure oldest sessions removed when limit hit
- [ ] **Load test auth system** - Verify performance with multiple users
- [ ] **Security review** - Validate all auth flows are secure

---

## 📋 **Completion Criteria**

### **Phase 1 Complete When:**
- All current auth flows work end-to-end
- No errors in login/logout/dashboard access
- Session data correctly populated from backend

### **Phase 2 Complete When:**
- Database doesn't accumulate expired tokens
- Users can revoke all sessions for security
- Reasonable session limits prevent abuse
- All new endpoints follow Simple, Uniform, Consistent patterns

### **Phase 3 Complete When:**
- All session management features tested
- Performance meets requirements  
- Security review passes
- Documentation updated

---

## 📝 **Notes**

**Current Status:** Testing current implementation before improvements

**Next Steps:** 
1. Complete Phase 1 testing
2. Implement session management in order of priority  
3. Test each improvement before moving to next

**Principle Reminder:** Simple ≠ "not good". Simple = elegant, maintainable, excellent.

---

*This TODO list follows the Simple, Uniform, Consistent doctrine - clear priorities, manageable tasks, measurable outcomes.*