package com.babycrttv.emeraldlegendswiki;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import org.json.JSONObject;

/**
 * Minimal site companion, not a game launcher or a ROM patcher.
 * This app only reads the curated public wiki over HTTPS.
 */
public final class MainActivity extends Activity {
    private static final String HOME = "https://babycrttv.github.io/pokeemerald-emerald-legends/wiki/";
    private static final String TRUSTED_HOST = "babycrttv.github.io";
    private static final String UPDATE_MANIFEST = "https://babycrttv.github.io/pokeemerald-emerald-legends/wiki/android-version.json";
    private static final String TRUSTED_PATH = "/pokeemerald-emerald-legends/wiki/";
    private WebView browser;
    private FrameLayout browserContainer;
    private LinearLayout offlinePanel;
    private boolean mainFrameFailed = false;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.rgb(244, 237, 251));
        getWindow().setNavigationBarColor(Color.rgb(244, 237, 251));
        getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
                | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);
        buildInterface();
        setupBrowser();
        if (savedInstanceState == null) {
            browser.loadUrl(HOME);
        } else {
            browser.restoreState(savedInstanceState);
        }
    }

    private int dp(int amount) {
        return Math.round(amount * getResources().getDisplayMetrics().density);
    }

    private Button makeButton(String label, String description) {
        Button button = new Button(this);
        button.setText(label);
        button.setTextSize(13);
        button.setAllCaps(false);
        button.setTextColor(Color.rgb(73, 48, 108));
        button.setContentDescription(description);
        button.setMinHeight(dp(48));
        return button;
    }

    private void buildInterface() {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setBackgroundColor(Color.rgb(248, 245, 255));

        LinearLayout top = new LinearLayout(this);
        top.setOrientation(LinearLayout.HORIZONTAL);
        top.setGravity(Gravity.CENTER_VERTICAL);
        top.setPadding(dp(9), 0, dp(9), 0);
        top.setBackgroundColor(Color.rgb(238, 228, 250));

        TextView brand = new TextView(this);
        brand.setText("✦  LEGENDS WIKI");
        brand.setTextSize(14);
        brand.setTypeface(null, 1);
        brand.setTextColor(Color.rgb(72, 49, 110));
        brand.setPadding(dp(8), 0, dp(4), 0);
        top.addView(brand, new LinearLayout.LayoutParams(0, dp(56), 1));
        brand.setGravity(Gravity.CENTER_VERTICAL);

        Button home = makeButton("⌂ Home", "Open wiki home");
        Button reload = makeButton("↻", "Reload current article");
        Button update = makeButton("↑ Update", "Check for an updated wiki app");
        home.setOnClickListener(v -> { hideOffline(); browser.loadUrl(HOME); });
        reload.setOnClickListener(v -> { hideOffline(); browser.reload(); });
        update.setOnClickListener(v -> checkForUpdates());
        top.addView(home, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, dp(52)));
        top.addView(reload, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, dp(52)));
        top.addView(update, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, dp(52)));
        layout.addView(top);

        browserContainer = new FrameLayout(this);
        browser = new WebView(this);
        browserContainer.addView(browser, new FrameLayout.LayoutParams(-1, -1));

        offlinePanel = new LinearLayout(this);
        offlinePanel.setOrientation(LinearLayout.VERTICAL);
        offlinePanel.setGravity(Gravity.CENTER);
        offlinePanel.setPadding(dp(28), dp(24), dp(28), dp(24));
        offlinePanel.setBackgroundColor(Color.rgb(248, 245, 255));
        TextView notice = new TextView(this);
        notice.setText("No connection to the Legends Wiki\n\nYour articles are hosted online and updated only when the project owner publishes a wiki revision. Connect to the internet and try again.");
        notice.setTextSize(17);
        notice.setGravity(Gravity.CENTER);
        notice.setTextColor(Color.rgb(69, 52, 94));
        offlinePanel.addView(notice);
        Button retry = makeButton("Try again", "Retry loading the wiki");
        retry.setOnClickListener(v -> { hideOffline(); browser.loadUrl(HOME); });
        offlinePanel.addView(retry);
        offlinePanel.setVisibility(View.GONE);
        browserContainer.addView(offlinePanel, new FrameLayout.LayoutParams(-1, -1));
        layout.addView(browserContainer, new LinearLayout.LayoutParams(-1, 0, 1));
        setContentView(layout);
    }

    private boolean isWikiUri(Uri uri) {
        return "https".equalsIgnoreCase(uri.getScheme())
                && TRUSTED_HOST.equalsIgnoreCase(uri.getHost())
                && uri.getPath() != null
                && uri.getPath().startsWith(TRUSTED_PATH);
    }

    private void openExternal(Uri uri) {
        if (!"https".equalsIgnoreCase(uri.getScheme())
                && !"http".equalsIgnoreCase(uri.getScheme())) {
            return;
        }
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, uri)
                    .addCategory(Intent.CATEGORY_BROWSABLE));
        } catch (ActivityNotFoundException e) {
            Toast.makeText(this, "No browser is available to open this link.", Toast.LENGTH_LONG).show();
        }
    }

    private long installedVersionCode() {
        try {
            android.content.pm.PackageInfo info = getPackageManager().getPackageInfo(getPackageName(), 0);
            return Build.VERSION.SDK_INT >= 28 ? info.getLongVersionCode() : info.versionCode;
        } catch (Exception ignored) {
            return 1;
        }
    }

    private void checkForUpdates() {
        Toast.makeText(this, "Checking for wiki updates…", Toast.LENGTH_SHORT).show();
        new Thread(() -> {
            HttpURLConnection connection = null;
            try {
                URL manifest = new URL(UPDATE_MANIFEST + "?t=" + System.currentTimeMillis());
                connection = (HttpURLConnection)manifest.openConnection();
                connection.setConnectTimeout(8000);
                connection.setReadTimeout(8000);
                connection.setUseCaches(false);
                if (connection.getResponseCode() != 200)
                    throw new IllegalStateException("Update service unavailable");
                StringBuilder body = new StringBuilder();
                try (BufferedReader br = new BufferedReader(
                        new InputStreamReader(connection.getInputStream(), "UTF-8"))) {
                    String line;
                    while ((line = br.readLine()) != null) body.append(line);
                }
                JSONObject release = new JSONObject(body.toString());
                final long latest = release.getLong("versionCode");
                final String version = release.getString("version");
                final String link = release.getString("url");
                final boolean temporarySignature =
                    "ephemeral-debug".equals(release.optString("signing"));
                runOnUiThread(() -> {
                    if (latest <= installedVersionCode()) {
                        new AlertDialog.Builder(this).setTitle("Wiki is up to date")
                                .setMessage("You're using the latest Legends Wiki app (" + version + "). No update is needed.")
                                .setPositiveButton("OK", null).show();
                    } else {
                        String warning = temporarySignature
                            ? "\n\nNote: This APK uses a temporary signing key. Android may require uninstalling an older build before installation."
                            : "";
                        new AlertDialog.Builder(this).setTitle("Wiki update available")
                                .setMessage("Latest version: " + version +
                                        "\nYour installed build: " + installedVersionCode() +
                                        "\n\nDownload the newest APK? Android will ask you to approve installation." + warning)
                                .setNegativeButton("Later", null)
                                .setPositiveButton("Download", (d,w) -> openExternal(Uri.parse(link)))
                                .show();
                    }
                });
            } catch (Exception error) {
                runOnUiThread(() -> new AlertDialog.Builder(this)
                        .setTitle("Can't check for updates")
                        .setMessage("Check your connection and try again. No changes were installed.")
                        .setPositiveButton("OK", null).show());
            } finally {
                if (connection != null) connection.disconnect();
            }
        }).start();
    }

    private void setupBrowser() {
        WebSettings settings = browser.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setUserAgentString(settings.getUserAgentString() + " LegendsWikiAndroid/" + installedVersionCode());
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setJavaScriptCanOpenWindowsAutomatically(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);
        settings.setSupportZoom(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);

        browser.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
                mainFrameFailed = false;
                hideOffline();
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if (isWikiUri(uri)) return false;
                // Block untrusted frames and route external destinations to the user's browser.
                if (request.isForMainFrame()) openExternal(uri);
                return true;
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                if (request.isForMainFrame()) { mainFrameFailed = true; showOffline(); }
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                if (!mainFrameFailed && isWikiUri(Uri.parse(url)) && view.getProgress() == 100) {
                    // The site's own article JSON handler displays offline guidance if its fetch fails.
                    hideOffline();
                }
            }
        });
    }

    private void showOffline() {
        offlinePanel.setVisibility(View.VISIBLE);
    }

    private void hideOffline() {
        offlinePanel.setVisibility(View.GONE);
    }

    @Override
    public void onBackPressed() {
        if (offlinePanel.getVisibility() == View.VISIBLE) {
            hideOffline();
            browser.loadUrl(HOME);
        } else if (browser.canGoBack()) {
            browser.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle state) {
        browser.saveState(state);
        super.onSaveInstanceState(state);
    }

    @Override
    protected void onDestroy() {
        if (browser != null) {
            browserContainer.removeView(browser);
            browser.destroy();
        }
        super.onDestroy();
    }
}
