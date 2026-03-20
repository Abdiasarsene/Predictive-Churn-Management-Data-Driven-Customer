# Moduls required imported
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
import logging

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== MIDDLEWARE SETUP ======
def apply_security_middleware(app:FastAPI):
    try:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True, 
            allow_methods=["*"],
            allow_headers=["*"]
        )
        
        app.add_middleware(
            TrustedHostMiddleware,
            # allowed_hosts=["localhost", "*.yourdomain.com"]
            allowed_hosts=["*"]

        )
        logger.info("✅ Middleware Applied")
    except Exception as e:
        logger.error(f"❌ Error applying security middleware : {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Middleware setup failed")

# ====== TOKEN CHECKER ======
def verify_token(token: str = Depends(oauth2_schema)):
    try:
        if token != "secrettoken123":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid or missing token",
                headers={"WWW-Authenticate" : "Bearer"}
            )
            logger.info("✅ Token succeded")
            return {"user" : "authenticated"}
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}", exc_info=True)
# end def