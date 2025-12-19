# Non-Working AISEARCH Providers

This document details the AISEARCH providers that are currently not working in the webscout library.

## Genspark

**Issue**: Unicode encoding issues
**Error**: `'charmap' codec can't encode characters`
**Details**: The provider encounters encoding problems when trying to process certain Unicode characters in the response.

## Perplexity

**Issue**: API connectivity problem
**Error**: `API returned status code 502`
**Details**: The Perplexity API is returning a 502 Bad Gateway error, indicating a server-side issue or that the endpoint may have changed.

## Stellar

**Issue**: Endpoint not found
**Error**: `404 Not Found`
**Details**: The Stellar API endpoint appears to be deprecated or moved, resulting in a 404 error when attempting to connect.

## Recommendations

1. Contact the webscout maintainers to report these issues
2. Check if the API endpoints have changed for Perplexity and Stellar
3. Investigate the Unicode encoding handling in the Genspark provider
4. Consider removing or temporarily disabling these providers until the issues are resolved