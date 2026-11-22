package com.unanx.browser.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.platform.LocalContext
import com.unanx.browser.browser.TabManager
import com.unanx.browser.data.AppDatabase
import com.unanx.browser.ui.screens.BrowserScreen
import com.unanx.browser.ui.screens.HomeScreen
import com.unanx.browser.ui.screens.SettingsScreen
import com.unanx.browser.util.UrlUtils

@Composable
fun BrowserApp(darkTheme: Boolean, onThemeChange: (Boolean) -> Unit) {
    val context = LocalContext.current
    val db = remember { AppDatabase.getInstance(context) }
    val tabManager = remember { TabManager() }
    var showSettings by remember { mutableStateOf(false) }
    val activeTab = tabManager.getActiveTab()

    when {
        showSettings -> SettingsScreen(
            db = db, darkTheme = darkTheme,
            onToggleTheme = onThemeChange,
            onBack = { showSettings = false }
        )
        activeTab == null || activeTab.url.isEmpty() -> HomeScreen(
            onSearch = { q -> activeTab?.url = UrlUtils.toUrlOrSearch(q) },
            onOpenSettings = { showSettings = true }
        )
        else -> BrowserScreen(
            activeTab = activeTab,
            tabManager = tabManager,
            db = db,
            onOpenSettings = { showSettings = true }
        )
    }
}
