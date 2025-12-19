# TTI Provider Fix Tasks

This document contains detailed tasks to fix non-working Text-to-Image (TTI) providers in `webscout/Provider/TTI/`.

**Test Date:** 2025-12-19  
**Working Providers:** ClaudeOnlineTTI, MagicStudioAI, PollinationsAI  
**Providers Requiring Fixes:** 9

---

## 1. AIArta (`aiarta.py`)

**Error:** `Failed to obtain authentication token`

**Issue:** The Firebase anonymous authentication is failing. The provider uses Google Identity Toolkit to get an anonymous auth token.

**Investigation Steps:**
1. Check if the Firebase API key `AIzaSyB3-71wG0fIt0shj0ee4fvx1shcjJHGrrQ` is still valid
2. Verify the auth URL `https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser` is correct
3. Check if ai-arta.com has updated their authentication mechanism
4. Inspect network requests on https://ai-arta.com using browser DevTools to see current auth flow

**Fix Approach:**
- Visit ai-arta.com in browser, open DevTools Network tab
- Generate an image and capture the authentication requests
- Update the `_get_auth_token()` method with the new auth flow
- May need to update headers, endpoints, or request payload

---

## 2. GPT1Image (`gpt1image.py`)

**Error:** `HTTPSConnectionPool(host='gpt1image.exomlapi.com', port=443): Max retries exceeded - NameResolutionError`

**Issue:** The domain `gpt1image.exomlapi.com` is unreachable/doesn't resolve.

**Investigation Steps:**
1. Check if the service has moved to a new domain
2. Search for "gpt1image" or "exomlapi" to find the new endpoint
3. Check if the service is permanently discontinued

**Fix Approach:**
- If new domain found: Update `self.api_endpoint` in `__init__`
- If service discontinued: Mark `working = False` permanently and document in docstring
- Consider finding an alternative free GPT-image API

---

## 3. ImagenAI (`imagen.py`)

**Error:** `HTTPSConnectionPool(host='imagen.exomlapi.com', port=443): Max retries exceeded - NameResolutionError`

**Issue:** The domain `imagen.exomlapi.com` is unreachable/doesn't resolve.

**Investigation Steps:**
1. Same as GPT1Image - appears to be same provider (exomlapi.com)
2. Check if exomlapi.com services have migrated

**Fix Approach:**
- Find new endpoint or mark as permanently non-working
- Consider integrating with official Google Imagen API (requires auth)

---

## 4. InfipAI (`infip.py`)

**Error:** `404 Client Error: Not Found for url: https://api.infip.pro/generate`

**Issue:** The API endpoint `/generate` no longer exists.

**Investigation Steps:**
1. Visit https://infip.pro to check if service is still active
2. Check API documentation for new endpoints
3. Inspect network requests when using the service in browser

**Fix Approach:**
- Update `self.api_endpoint` with correct endpoint
- May need to update request payload structure
- Check if authentication is now required

---

## 5. MonoChatAI (`monochat.py`)

**Error:** `403 Client Error: Forbidden for url: https://gg.is-a-furry.dev/api/image`

**Issue:** The API is returning 403 Forbidden - likely requires authentication or has IP/rate limiting.

**Investigation Steps:**
1. Check if the service requires authentication now
2. Verify headers are correct (User-Agent, Origin, Referer)
3. Check if there's CORS or origin validation
4. Test if the endpoint works from browser

**Fix Approach:**
- Add proper authentication headers if required
- Update Origin/Referer headers to match expected values
- May need to add session cookies or tokens
- Check for Cloudflare or similar protection

---

## 6. PiclumenAI (`piclumen.py`)

**Error:** `HTTPSConnectionPool(host='s9.piclumen.art', port=443): Read timed out (read timeout=60)`

**Issue:** The server is not responding within 60 seconds - could be slow or blocked.

**Investigation Steps:**
1. Check if piclumen.art is still active
2. Test the endpoint from browser
3. Check if different server endpoints (s1, s2, etc.) work
4. Verify if the session initialization is correct

**Fix Approach:**
- Try alternative server endpoints if available
- Increase timeout for slow operations
- Check if the API flow has changed (session creation, image generation, polling)
- Verify WebSocket or SSE isn't required now

---

## 7. PixelMuse (`pixelmuse.py`)

**Error:** `401 Client Error: Unauthorized for url: https://www.pixelmuse.studio/api/predictions`

**Issue:** The API now requires authentication.

**Investigation Steps:**
1. Visit pixelmuse.studio and check if free tier still exists
2. Check if guest/anonymous tokens are available
3. Inspect network requests for authentication headers
4. Check if session cookies are required

**Fix Approach:**
- Implement session-based authentication if available
- Add required authentication headers
- If paid-only now: set `required_auth = True` and add API key parameter
- Document authentication requirements in docstring

---

## 8. TogetherImage (`together.py`)

**Error:** `Together.xyz API error: Invalid API key provided`

**Issue:** The automatic API key fetching from codegeneration.ai is failing.

**Investigation Steps:**
1. Check if `https://codegeneration.ai/api/get/toghether` endpoint still works
2. Verify the API key activation flow
3. Test with a manually provided Together.xyz API key

**Fix Approach:**
- Fix the `_get_api_key()` method to use working endpoint
- Add fallback API key sources
- Allow users to provide their own API key as parameter
- Consider making `required_auth = True` and requiring user API key

---

## 9. VeniceAI (`venice.py`)

**Error:** `400 Client Error: Bad Request for url: https://outerface.venice.ai/api/inference/image`

**Issue:** The request payload or headers are incorrect for the current API version.

**Investigation Steps:**
1. Visit venice.ai and test image generation
2. Capture network requests to see current API format
3. Compare request payload with what the provider sends
4. Check if new required fields were added

**Fix Approach:**
- Update request payload structure to match current API
- Add any new required headers
- Update model names if changed
- Fix aspect ratio or size parameter format

---

## General Investigation Tips

1. **Browser DevTools:** Open the website, go to Network tab, generate an image, and capture all requests
2. **Check for Cloudflare:** Look for `cf-` headers or JavaScript challenges
3. **Session Management:** Many sites now require proper session initialization
4. **Rate Limiting:** Some failures may be temporary due to rate limits
5. **API Versioning:** Check if `/v1/`, `/v2/` endpoints exist

## Priority Order

1. **High Priority (likely easy fixes):**
   - VeniceAI (400 Bad Request - probably payload issue)
   - InfipAI (404 - endpoint moved)
   - MonoChatAI (403 - headers issue)

2. **Medium Priority:**
   - AIArta (auth flow update needed)
   - PiclumenAI (timeout - flow may have changed)
   - PixelMuse (auth required)

3. **Low Priority (may be discontinued):**
   - GPT1Image (domain unreachable)
   - ImagenAI (domain unreachable)
   - TogetherImage (API key service failing)

