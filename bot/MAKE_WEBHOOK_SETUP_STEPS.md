# 🎯 Make.com Webhook Setup - Step by Step

## Current Status

✅ **Webhook URL Configured:** `https://hook.us2.make.com/swbxqjfozsiwbyuforw60gxmwufcjwtw`

✅ **Test Results:**
- Environment configuration: ✅ PASS
- Webhook connectivity: ✅ PASS (410 error is expected - scenario not listening yet)
- Performance: ✅ PASS (0.89 seconds response time)

⚠️ **Next Step:** Create Make.com scenario to listen for webhook

---

## Step 1: Create a New Make.com Scenario

1. Go to [Make.com](https://make.com)
2. Click **Create a new scenario**
3. Name it: `Recon Automation Bot`
4. Click **Create**

---

## Step 2: Add Custom Webhook Trigger

1. In the scenario editor, click the **+** button to add a module
2. Search for **Custom Webhook**
3. Click to add it as the trigger
4. Click **Save**
5. You'll see a webhook URL - **DO NOT COPY IT** (we already have one)
6. Click **OK** to confirm

---

## Step 3: Add Gemini AI Module

1. Click the **+** button after the webhook module
2. Search for **HTTP Request**
3. Click to add it
4. Configure:
   - **URL:** `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent`
   - **Method:** POST
   - **Headers:** 
     - Key: `Content-Type`
     - Value: `application/json`
   - **Body:**
     ```json
     {
       "contents": [{
         "parts": [{
           "text": "Analyze these recon results and provide a security summary:\n\n{{1.files}}"
         }]
       }]
     }
     ```
   - **Query String:**
     - Key: `key`
     - Value: `YOUR_GEMINI_API_KEY`

5. Click **OK**

---

## Step 4: Add Google Docs Module

1. Click the **+** button after the HTTP module
2. Search for **Google Docs**
3. Click to add it
4. Click **Authorize** to connect your Google account
5. Configure:
   - **Action:** Create a document
   - **Title:** `Recon Report - {{1.target_domain}} - {{now}}`
   - **Content:** `{{2.body}}`
   - **Folder:** Select your preferred folder

6. Click **OK**

---

## Step 5: Add Router for Error Handling (Optional)

1. Click the **+** button after Google Docs
2. Search for **Router**
3. Click to add it
4. This will help handle errors gracefully

---

## Step 6: Save and Activate Scenario

1. Click **Save** button (top right)
2. Toggle the **ON/OFF** switch to **ON** (turn on the scenario)
3. You should see a green checkmark

---

## Step 7: Test the Webhook

Now that the scenario is listening, run the test again:

```bash
python test_webhook.py
```

### Expected Output:

```
✅ HTTP Status: 200
✅ Webhook received successfully!
✅ Google Doc created: https://docs.google.com/document/d/...
```

---

## Webhook Payload Structure

The webhook will receive this JSON:

```json
{
  "target_domain": "example.com",
  "files": [
    {
      "name": "amass_results.txt",
      "content": "subdomains..."
    },
    {
      "name": "shodan_results.json",
      "content": "{...}"
    },
    {
      "name": "nmap_results.txt",
      "content": "ports..."
    }
  ],
  "timestamp": "2025-10-27T11:18:47.793326"
}
```

---

## Troubleshooting

### Issue: Still getting 410 error

**Check:**
1. Scenario is toggled **ON** (green switch)
2. Custom Webhook module is in the scenario
3. Webhook URL matches exactly

**Solution:**
1. Go to Make.com scenario
2. Check the ON/OFF toggle is green
3. Regenerate webhook URL if needed

### Issue: 500 error from Gemini

**Check:**
1. Gemini API key is valid
2. API is enabled in Google Cloud
3. API key has correct permissions

**Solution:**
1. Get new API key from [Google Cloud Console](https://console.cloud.google.com)
2. Update .env file with new key
3. Update Make.com HTTP module with new key

### Issue: Google Docs not created

**Check:**
1. Google account is authorized
2. Folder permissions are correct
3. Google Docs API is enabled

**Solution:**
1. Re-authorize Google account in Make.com
2. Check folder permissions
3. Enable Google Docs API in Google Cloud

---

## Make.com Scenario Flow

```
Webhook (Trigger)
    ↓
HTTP Request (Gemini API)
    ↓
Google Docs (Create Document)
    ↓
Router (Error Handling)
    ↓
Output (Document URL)
```

---

## Testing Checklist

- [ ] Make.com account created
- [ ] New scenario created
- [ ] Custom Webhook added
- [ ] HTTP Request module added
- [ ] Google Docs module added
- [ ] Scenario is toggled ON
- [ ] Run `python test_webhook.py`
- [ ] Check for ✅ PASS messages
- [ ] Verify Google Doc was created

---

## Next Steps

1. **Create Make.com scenario** (follow steps above)
2. **Activate scenario** (toggle ON)
3. **Run webhook test:** `python test_webhook.py`
4. **Verify Google Doc** in Google Drive
5. **Run full pipeline:** `python recon_automation_bot.py example.com`

---

## Quick Reference

**Webhook URL:**
```
https://hook.us2.make.com/swbxqjfozsiwbyuforw60gxmwufcjwtw
```

**Test Command:**
```bash
python test_webhook.py
```

**Full Pipeline:**
```bash
python recon_automation_bot.py example.com
```

---

## Support

- **Make.com Help:** https://www.make.com/en/help
- **Google Docs API:** https://developers.google.com/docs/api
- **Gemini API:** https://ai.google.dev/

---

**Status:** ✅ Webhook configured and tested
**Next:** Create Make.com scenario to listen for webhook

