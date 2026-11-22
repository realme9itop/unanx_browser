package com.unanx.browser.browser

import android.webkit.WebView
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import java.util.UUID

class BrowserTab(
    val id: String = UUID.randomUUID().toString(),
    initialUrl: String = "",
    val isIncognito: Boolean = false
) {
    var url by mutableStateOf(initialUrl)
    var title by mutableStateOf("New Tab")
    var webView: WebView? = null
}

class TabManager {
    val tabs = mutableStateListOf<BrowserTab>()
    var activeTabIndex by mutableStateOf(0)

    init { addTab() }

    fun addTab(incognito: Boolean = false): BrowserTab {
        val tab = BrowserTab(isIncognito = incognito)
        tabs.add(tab)
        activeTabIndex = tabs.lastIndex
        return tab
    }

    fun closeTab(index: Int) {
        if (tabs.size <= 1) return
        tabs[index].webView?.destroy()
        tabs.removeAt(index)
        if (activeTabIndex >= tabs.size) activeTabIndex = tabs.lastIndex
    }

    fun getActiveTab(): BrowserTab? = tabs.getOrNull(activeTabIndex)
}
