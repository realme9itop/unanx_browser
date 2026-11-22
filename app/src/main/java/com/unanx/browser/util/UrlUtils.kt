package com.unanx.browser.util

import android.webkit.URLUtil

object UrlUtils {
    private const val SEARCH_ENGINE = "https://duckduckgo.com/?q="

    fun toUrlOrSearch(input: String): String {
        val trimmed = input.trim()
        if (trimmed.isEmpty()) return "about:blank"
        return when {
            URLUtil.isNetworkUrl(trimmed) -> trimmed
            trimmed.contains(".") && !trimmed.contains(" ") -> "https://$trimmed"
            else -> SEARCH_ENGINE + java.net.URLEncoder.encode(trimmed, "UTF-8")
        }
    }
}
