package com.unanx.browser.browser

import android.graphics.Bitmap
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient

class UnanxWebViewClient(
    private val onPageFinished: (String?) -> Unit = {}
) : WebViewClient() {
    override fun shouldInterceptRequest(view: WebView?, request: WebResourceRequest?): WebResourceResponse? {
        val url = request?.url?.toString() ?: return null
        return if (AdBlocker.shouldBlock(url)) {
            AdBlocker.incrementBlocked()
            AdBlocker.createEmptyResponse()
        } else super.shouldInterceptRequest(view, request)
    }
    override fun onPageFinished(view: WebView?, url: String?) {
        super.onPageFinished(view, url)
        onPageFinished(url)
    }
}
