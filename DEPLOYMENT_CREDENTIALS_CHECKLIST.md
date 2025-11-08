# 📋 Deployment Credentials Checklist

## Required Credentials and Information for Hostinger VPS Deployment

Before starting the deployment, gather all the following information:

---

## 🌐 **1. VPS/Server Information**

- [ ] **VPS IP Address**: `_________________`
  - Example: `123.45.67.89`
  - Found in Hostinger control panel

- [ ] **SSH Username**: `_________________`
  - Usually `root` or a custom username
  - Default Hostinger VPS: `root`

- [ ] **SSH Password**: `_________________`
  - Your VPS root password
  - Or SSH private key path if using key authentication

- [ ] **Domain Name**: `_________________`
  - Example: `madboost.gg` or `www.madboost.gg`
  - Must point to your VPS IP address (DNS configured)

---

## 🔐 **2. Django Security Settings**

- [ ] **Django Secret Key**: `_________________`
  - Generate using: 
    ```bash
    python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```
  - **OR** use openssl:
    ```bash
    openssl rand -base64 32
    ```
  - **IMPORTANT**: Must be unique and secret!

- [ ] **Debug Mode**: `False` (for production)
  - Will be set automatically in `.env`

---

## 🗄️ **3. Database Credentials**

- [ ] **Database Name**: `gameboosters_db01` (default)
  - Or custom name: `_________________`

- [ ] **Database User**: `postgres` (default)
  - Or custom user: `_________________`

- [ ] **Database Password**: `_________________`
  - **MUST BE STRONG** - at least 16 characters
  - Example: `My$tr0ng!P@ssw0rd123`
  - ⚠️ **This will be used in Docker, so make it secure**

---

## 📧 **4. Email Configuration (SMTP)**

- [ ] **Email Host**: `smtp.office365.com` (default)
  - Or Gmail: `smtp.gmail.com`
  - Or custom: `_________________`

- [ ] **Email Port**: `587` (default for TLS)
  - Or `465` for SSL
  - Custom: `_________________`

- [ ] **Email Username**: `_________________`
  - Your full email address
  - Example: `no-reply@madboost.gg`

- [ ] **Email Password**: `_________________`
  - Your email account password
  - Or app-specific password if using Gmail

- [ ] **Default From Email**: `_________________`
  - Usually same as Email Username
  - Example: `no-reply@madboost.gg`

---

## 🔗 **5. Social Authentication (Google OAuth)**

- [ ] **Google OAuth Client ID**: `_________________`
  - Get from: https://console.cloud.google.com/apis/credentials
  - Example: `YOUR_CLIENT_ID.apps.googleusercontent.com`

- [ ] **Google OAuth Client Secret**: `_________________`
  - Get from same Google Cloud Console
  - Example: `GOCSPX-YOUR_CLIENT_SECRET_HERE`

- [ ] **Google OAuth Redirect URI**: `https://your-domain.com/social/complete/google-oauth2/`
  - Replace `your-domain.com` with your actual domain
  - Example: `https://madboost.gg/social/complete/google-oauth2/`

---

## 💳 **6. Payment Gateway Credentials**

### Cryptomus (if using)

- [ ] **Payment Key**: `_________________`
  - From Cryptomus dashboard
  - Also called API Key

- [ ] **Merchant UUID**: `_________________`
  - From Cryptomus dashboard
  - Your merchant identifier

### PayPal (if using)

- [ ] **PayPal Client ID**: `_________________`
  - From PayPal Developer Dashboard
  - For production (not sandbox)

- [ ] **PayPal Client Secret**: `_________________`
  - From PayPal Developer Dashboard
  - For production (not sandbox)

- [ ] **PayPal Mode**: `live` (for production)
  - Or `sandbox` for testing

---

## 🔒 **7. SSL Certificate (Let's Encrypt)**

- [ ] **Domain for SSL**: `_________________`
  - Primary domain: `your-domain.com`
  - With www: `www.your-domain.com`

- [ ] **Email for SSL Certificate**: `_________________`
  - Used by Let's Encrypt for expiration notices
  - Example: `admin@madboost.gg`

- [ ] **DNS Status**: ✅ **Verified**
  - Domain must point to your VPS IP before SSL setup
  - Check with: `dig your-domain.com` or `nslookup your-domain.com`

---

## 📝 **8. Additional Settings**

- [ ] **Media URL Path**: `/media/` (default)
  - Or custom: `_________________`

- [ ] **Redis Usage**: `True` (enabled by default)
  - For WebSocket/Channels support

---

## ✅ **Quick Checklist Summary**

Before deployment, you need:

1. ✅ VPS IP address and SSH access
2. ✅ Domain name (DNS configured)
3. ✅ Django SECRET_KEY (generate new one)
4. ✅ Database password (strong password)
5. ✅ Email credentials (SMTP)
6. ✅ Google OAuth credentials (if using)
7. ✅ Payment gateway credentials (if using)
8. ✅ SSL email (for Let's Encrypt)

---

## 🎯 **Pre-Deployment Checklist**

Before running the deployment script:

- [ ] All credentials above are gathered
- [ ] Domain DNS is configured and pointing to VPS IP
- [ ] VPS has SSH access working
- [ ] You have root or sudo access
- [ ] Django SECRET_KEY is generated
- [ ] Database password is strong and secure
- [ ] Email SMTP credentials are correct
- [ ] Google OAuth redirect URI is configured in Google Console
- [ ] Payment gateway credentials are ready (if applicable)

---

## 📞 **Where to Find Credentials**

### Hostinger VPS
- **IP Address**: Hostinger control panel → VPS → Server Details
- **SSH Password**: Hostinger control panel → VPS → Access Details
- **Root Access**: Usually `root` user

### Google OAuth
- **Console**: https://console.cloud.google.com/
- **APIs & Services** → **Credentials** → Create OAuth 2.0 Client ID
- **Authorized redirect URIs**: Add your production domain

### Email (Office 365)
- **SMTP Settings**: Usually same as your email login
- **App Password**: If 2FA enabled, create app-specific password

### PayPal
- **Dashboard**: https://developer.paypal.com/
- **My Apps & Credentials** → Create new app for production

### Cryptomus
- **Dashboard**: https://cryptomus.com/
- **API Settings** → Get Payment Key and Merchant UUID

---

## ⚠️ **Security Notes**

1. **Never commit `.env` file to Git** - it contains sensitive credentials
2. **Use strong passwords** - especially for database
3. **Generate new SECRET_KEY** - don't use the example one
4. **Keep credentials secure** - store them safely offline
5. **Update credentials regularly** - especially after deployment

---

## 🚀 **Ready to Deploy?**

Once you have all the credentials above, you can proceed with deployment:

1. SSH into your VPS
2. Run the deployment script
3. Update `.env` file with your credentials
4. Build and start containers

See `HOSTINGER_VPS_DEPLOYMENT.md` for detailed deployment steps.

