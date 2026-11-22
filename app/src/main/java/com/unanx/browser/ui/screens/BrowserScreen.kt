package com.unanx.browser.ui.screens

import android.annotation.SuppressLint
import android.app.DownloadManager
import android.content.Context
import android.net.Uri
import android.os.Environment
import android.webkit.CookieManager
import android.webkit.WebView
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.viewinterop.AndroidView
import com.unanx.browser.browser.BrowserTab
import com.unanx.browser.browser.TabManager
import com.unanx.browser.browser.UnanxWebViewClient
import com.unanx.browser.data.AppDatabase
import com.unanx.browser.data.HistoryEntity
import com.unanx.browser.ui.components.AddressBar
import com.unanx.browser.ui.components.TabBar
import com.unanx.browser.util.UrlUtils
import kotlinx.coroutines.launch

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun BrowserScreen(
    activeTab: BrowserTab,
    tabManager: TabManager,
    db: AppDatabase,
    onOpenSettings: () -> Unit
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()

    key(activeTab.id) {
        if (activeTab.webView == null) {
            activeTab.webView = WebView(context).apply {
                settings.javaScriptEnabled = true
                settings.domStorageEnabled = true
                webViewClient = UnanxWebViewClient(
                    onPageFinished = { url ->
                        if (url != null && !activeTab.isIncognito && !url.startsWith("about:")) {
                            scope.launch {
                                db.historyDao().insert(HistoryEntity(url = url, title = url))
                            }
                        }
                    }
                )
                setDownloadListener { url, ua, cd, mime, _ ->
                    val req = DownloadManager.Request(Uri.parse(url))
                    req.setMimeType(mime)
                    req.addRequestHeader("User-Agent", ua)
                    req.setTitle(android.webkit.URLUtil.guessFileName(url, cd, mime))
                    req.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                    req.setDestinationInExternalPublicDir(
                        Environment.DIRECTORY_DOWNLOADS,
                        android.webkit.URLUtil.guessFileName(url, cd, mime)
                    )
                    (context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager).enqueue(req)
                }
                CookieManager.getInstance().setAcceptCookie(!activeTab.isIncognito)
                loadUrl(activeTab.url)
            }
        }

        Column(modifier = Modifier.fillMaxSize()) {
            TabBar(tabManager)
            AddressBar(
                initialUrl = activeTab.url,
                onNavigate = { input ->
                    val url = UrlUtils.toUrlOrSearch(input)
                    activeTab.url = url
                    activeTab.webView?.loadUrl(url)
                },
                onBack = { activeTab.webView?.goBack() },
                onForward = { activeTab.webView?.goForward() },
                onReload = { activeTab.webView?.reload() },
                onHome = { activeTab.url = "" },
                onSettings = onOpenSettings
            )
            AndroidView(factory = { activeTab.webView!! }, modifier = Modifier.weight(1f))
        }
    }
}
