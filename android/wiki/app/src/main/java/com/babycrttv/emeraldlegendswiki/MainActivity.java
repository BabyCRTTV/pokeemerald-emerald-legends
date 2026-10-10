package com.babycrttv.emeraldlegendswiki;

import android.app.Activity;
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
        getWindow().setStatusBarColor(Color.rgb(231, 242, 232));
        getWindow().setNavigationBarColor(Color.rgb(231, 242, 232));
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
        layout.setBackgroundColor(Color.rgb(246, 250, 245));

        browserContainer = new FrameLayout(this);
        browser = new WebView(this);
        browserContainer.addView(browser, new FrameLayout.LayoutParams(-1, -1));

        offlinePanel = new LinearLayout(this);
        offlinePanel.setOrientation(LinearLayout.VERTICAL);
        offlinePanel.setGravity(Gravity.CENTER);
        offlinePanel.setPadding(dp(28), dp(24), dp(28), dp(24));
        offlinePanel.setBackgroundColor(Color.rgb(246, 250, 245));
        TextView notice = new TextView(this);
        notice.setText("No connection to the Legends Wiki\n\nYour articles are hosted online and updated only when the project owner publishes a wiki revision. Connect to the internet and try again.");
        notice.setTextSize(17);
        notice.setGravity(Gravity.CENTER);
        notice.setTextColor(Color.rgb(39, 75, 55));
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
