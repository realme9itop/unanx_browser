package com.unanx.browser.browser

import android.webkit.WebResourceResponse
import java.io.ByteArrayInputStream

object AdBlocker {
    private val blockedHosts = setOf(
        "doubleclick.net", "googleadservices.com", "googlesyndication.com",
        "google-analytics.com", "adservice.google.com", "an.yandex.ru",
        "popunder.net", "popads.net", "propellerads.com", "onclickads.net",
        "adf.ly", "shorte.st", "exoclick.com", "juicyads.com",
        "trafficjunky.com", "adnxs.com", "adsrvr.org", "taboola.com",
        "outbrain.com", "criteo.com", "criteo.net", "scorecardresearch.com",
        "quantserve.com", "moatads.com", "amazon-adsystem.com", "advertising.com"
    )

    @Volatile var enabled: Boolean = true
        private set
    @Volatile var blockedCount: Int = 0
        private set

    fun toggle(): Boolean { enabled = !enabled; return enabled }

    fun shouldBlock(url: String): Boolean {
        if (!enabled) return false
        val host = try { java.net.URI(url).host ?: return false }
                   catch (e: Exception) { return false }
        return blockedHosts.any { host.contains(it, ignoreCase = true) }
    }

    fun incrementBlocked() { blockedCount++ }

    fun createEmptyResponse(): WebResourceResponse =
        WebResourceResponse("text/plain", "utf-8", ByteArrayInputStream(ByteArray(0)))
}
