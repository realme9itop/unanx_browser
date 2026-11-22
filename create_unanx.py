"""
Создаёт полный проект unanx (Android browser) в текущей директории.
Запуск: python create_unanx.py
"""
from pathlib import Path

FILES = {

"settings.gradle.kts": '''pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "unanx"
include(":app")
''',

"build.gradle.kts": '''plugins {
    id("com.android.application") version "8.5.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
    id("com.google.devtools.ksp") version "1.9.24-1.0.20" apply false
}
''',

"gradle.properties": '''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
''',

"app/build.gradle.kts": '''plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.google.devtools.ksp")
}

android {
    namespace = "com.unanx.browser"
    compileSdk = 34
    defaultConfig {
        applicationId = "com.unanx.browser"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }
    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.14" }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.06.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.activity:activity-compose:1.9.0")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.2")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.2")
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    ksp("androidx.room:room-compiler:2.6.1")
    implementation("androidx.core:core-splashscreen:1.0.1")
    implementation("androidx.webkit:webkit:1.11.0")
}
''',

"app/src/main/AndroidManifest.xml": '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="28" />
    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.Unanx.Splash">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.Unanx.Splash"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
''',

"app/src/main/java/com/unanx/browser/MainActivity.kt": '''package com.unanx.browser

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import com.unanx.browser.ui.BrowserApp
import com.unanx.browser.ui.theme.UnanxTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        installSplashScreen()
        super.onCreate(savedInstanceState)
        setContent {
            var darkTheme by remember { mutableStateOf(true) }
            UnanxTheme(darkTheme = darkTheme) {
                BrowserApp(
                    darkTheme = darkTheme,
                    onThemeChange = { darkTheme = it }
                )
            }
        }
    }
}
''',

"app/src/main/java/com/unanx/browser/ui/theme/Color.kt": '''package com.unanx.browser.ui.theme

import androidx.compose.ui.graphics.Color

val BlackBackground = Color(0xFF000000)
val BlackSurface = Color(0xFF121212)
val BlackOnBackground = Color(0xFFFFFFFF)
val SoftPink = Color(0xFFFF69B4)

val PinkBackground = Color(0xFFFFD1DC)
val PinkSurface = Color(0xFFFFE4E9)
val PinkOnBackground = Color(0xFF2B0918)
val HotPink = Color(0xFFE91E63)
''',

"app/src/main/java/com/unanx/browser/ui/theme/Theme.kt": '''package com.unanx.browser.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val BlackColorScheme = darkColorScheme(
    background = BlackBackground, surface = BlackSurface,
    onBackground = BlackOnBackground, onSurface = BlackOnBackground,
    primary = SoftPink, onPrimary = BlackBackground
)
private val PinkColorScheme = lightColorScheme(
    background = PinkBackground, surface = PinkSurface,
    onBackground = PinkOnBackground, onSurface = PinkOnBackground,
    primary = HotPink, onPrimary = PinkBackground
)

@Composable
fun UnanxTheme(darkTheme: Boolean = true, content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = if (darkTheme) BlackColorScheme else PinkColorScheme,
        typography = Typography,
        content = content
    )
}
''',

"app/src/main/java/com/unanx/browser/ui/theme/Type.kt": '''package com.unanx.browser.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val Typography = Typography(
    displayLarge = Typography().displayLarge.copy(
        fontFamily = FontFamily.Serif,
        fontWeight = FontWeight.Bold,
        fontSize = 72.sp
    )
)
''',

"app/src/main/java/com/unanx/browser/data/HistoryEntity.kt": '''package com.unanx.browser.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "history")
data class HistoryEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val url: String,
    val title: String,
    val timestamp: Long = System.currentTimeMillis()
)
''',

"app/src/main/java/com/unanx/browser/data/HistoryDao.kt": '''package com.unanx.browser.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface HistoryDao {
    @Insert suspend fun insert(history: HistoryEntity)
    @Query("SELECT * FROM history ORDER BY timestamp DESC") fun getAll(): Flow<List<HistoryEntity>>
    @Query("DELETE FROM history") suspend fun clearAll()
}
''',

"app/src/main/java/com/unanx/browser/data/BookmarkEntity.kt": '''package com.unanx.browser.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "bookmarks")
data class BookmarkEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val url: String,
    val title: String,
    val timestamp: Long = System.currentTimeMillis()
)
''',

"app/src/main/java/com/unanx/browser/data/BookmarkDao.kt": '''package com.unanx.browser.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface BookmarkDao {
    @Insert suspend fun insert(bookmark: BookmarkEntity)
    @Query("SELECT * FROM bookmarks ORDER BY timestamp DESC") fun getAll(): Flow<List<BookmarkEntity>>
    @Query("DELETE FROM bookmarks WHERE id = :id") suspend fun deleteById(id: Long)
}
''',

"app/src/main/java/com/unanx/browser/data/AppDatabase.kt": '''package com.unanx.browser.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [HistoryEntity::class, BookmarkEntity::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun historyDao(): HistoryDao
    abstract fun bookmarkDao(): BookmarkDao
    companion object {
        @Volatile private var INSTANCE: AppDatabase? = null
        fun getInstance(context: Context): AppDatabase =
            INSTANCE ?: synchronized(this) {
                Room.databaseBuilder(context.applicationContext, AppDatabase::class.java, "unanx.db")
                    .build().also { INSTANCE = it }
            }
    }
}
''',

"app/src/main/java/com/unanx/browser/browser/AdBlocker.kt": '''package com.unanx.browser.browser

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
''',

"app/src/main/java/com/unanx/browser/browser/UnanxWebViewClient.kt": '''package com.unanx.browser.browser

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
''',

"app/src/main/java/com/unanx/browser/browser/TabManager.kt": '''package com.unanx.browser.browser

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
''',

"app/src/main/java/com/unanx/browser/util/UrlUtils.kt": '''package com.unanx.browser.util

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
''',

"app/src/main/java/com/unanx/browser/ui/BrowserApp.kt": '''package com.unanx.browser.ui

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
''',

"app/src/main/java/com/unanx/browser/ui/screens/HomeScreen.kt": '''package com.unanx.browser.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun HomeScreen(onSearch: (String) -> Unit, onOpenSettings: () -> Unit) {
    var query by remember { mutableStateOf("") }
    Column(
        modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background).padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("unanx", fontFamily = FontFamily.Serif, fontSize = 72.sp,
             color = MaterialTheme.colorScheme.onBackground)
        Spacer(Modifier.height(32.dp))
        OutlinedTextField(
            value = query, onValueChange = { query = it },
            modifier = Modifier.fillMaxWidth(),
            placeholder = { Text("Поиск или URL") },
            leadingIcon = { Icon(Icons.Default.Search, null) },
            singleLine = true, shape = RoundedCornerShape(24.dp)
        )
        Spacer(Modifier.height(16.dp))
        Button(onClick = { if (query.isNotBlank()) onSearch(query) }, modifier = Modifier.fillMaxWidth()) {
            Text("Перейти")
        }
        Spacer(Modifier.height(32.dp))
        IconButton(onClick = onOpenSettings) { Icon(Icons.Default.Settings, "Настройки") }
    }
}
''',

"app/src/main/java/com/unanx/browser/ui/screens/BrowserScreen.kt": '''package com.unanx.browser.ui.screens

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
''',

"app/src/main/java/com/unanx/browser/ui/components/AddressBar.kt": '''package com.unanx.browser.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp

@Composable
fun AddressBar(
    initialUrl: String, onNavigate: (String) -> Unit,
    onBack: () -> Unit, onForward: () -> Unit, onReload: () -> Unit,
    onHome: () -> Unit, onSettings: () -> Unit
) {
    var text by remember(initialUrl) { mutableStateOf(initialUrl) }
    val kb = LocalSoftwareKeyboardController.current
    Row(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 4.dp, vertical = 2.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, null) }
        IconButton(onClick = onForward) { Icon(Icons.Default.ArrowForward, null) }
        OutlinedTextField(
            value = text, onValueChange = { text = it },
            modifier = Modifier.weight(1f), singleLine = true,
            shape = RoundedCornerShape(24.dp),
            keyboardOptions = KeyboardOptions(imeAction = ImeAction.Go),
            keyboardActions = KeyboardActions(onGo = { onNavigate(text); kb?.hide() })
        )
        IconButton(onClick = onReload) { Icon(Icons.Default.Refresh, null) }
        IconButton(onClick = onHome) { Icon(Icons.Default.Home, null) }
        IconButton(onClick = onSettings) { Icon(Icons.Default.Settings, null) }
    }
}
''',

"app/src/main/java/com/unanx/browser/ui/components/TabBar.kt": '''package com.unanx.browser.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.unanx.browser.browser.TabManager

@Composable
fun TabBar(tabManager: TabManager) {
    LazyRow(
        modifier = Modifier.fillMaxWidth().padding(4.dp),
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        itemsIndexed(tabManager.tabs) { index, tab ->
            AssistChip(
                onClick = { tabManager.activeTabIndex = index },
                label = { Text(tab.title.take(15), maxLines = 1) },
                trailingIcon = {
                    IconButton(onClick = { tabManager.closeTab(index) }, modifier = Modifier.size(16.dp)) {
                        Icon(Icons.Default.Close, null)
                    }
                },
                colors = if (index == tabManager.activeTabIndex)
                    AssistChipDefaults.assistChipColors(containerColor = MaterialTheme.colorScheme.primary)
                else AssistChipDefaults.assistChipColors()
            )
        }
        item { IconButton(onClick = { tabManager.addTab() }) { Icon(Icons.Default.Add, null) } }
    }
}
''',

"app/src/main/java/com/unanx/browser/ui/screens/SettingsScreen.kt": '''package com.unanx.browser.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.unanx.browser.browser.AdBlocker
import com.unanx.browser.data.AppDatabase
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    db: AppDatabase, darkTheme: Boolean,
    onToggleTheme: (Boolean) -> Unit, onBack: () -> Unit
) {
    var adBlockEnabled by remember { mutableStateOf(AdBlocker.enabled) }
    var blockedCount by remember { mutableStateOf(AdBlocker.blockedCount) }
    val scope = rememberCoroutineScope()

    Scaffold(topBar = {
        TopAppBar(
            title = { Text("Настройки") },
            navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, null) } }
        )
    }) { padding ->
        Column(modifier = Modifier.padding(padding).padding(16.dp)) {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("Тёмная тема (чёрная)")
                Switch(checked = darkTheme, onCheckedChange = onToggleTheme)
            }
            Spacer(Modifier.height(16.dp))
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("AdBlock (заблокировано: $blockedCount)")
                Switch(checked = adBlockEnabled, onCheckedChange = {
                    adBlockEnabled = AdBlocker.toggle()
                    blockedCount = AdBlocker.blockedCount
                })
            }
            Spacer(Modifier.height(16.dp))
            Button(onClick = { scope.launch { db.historyDao().clearAll() } }) {
                Text("Очистить историю")
            }
        }
    }
}
''',

"app/src/main/res/values/strings.xml": '''<resources>
    <string name="app_name">unanx</string>
</resources>
''',

"app/src/main/res/values/themes.xml": '''<resources>
    <style name="Theme.Unanx" parent="android:Theme.Material.NoActionBar">
        <item name="android:statusBarColor">@android:color/black</item>
    </style>
    <style name="Theme.Unanx.Splash" parent="Theme.SplashScreen">
        <item name="windowSplashScreenBackground">@android:color/black</item>
        <item name="windowSplashScreenAnimatedIcon">@drawable/ic_launcher_foreground</item>
        <item name="postSplashScreenTheme">@style/Theme.Unanx</item>
    </style>
</resources>
''',

"app/src/main/res/drawable/ic_launcher_foreground.xml": '''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#FF69B4"
        android:pathData="M30,40 L40,40 L40,60 L50,40 L60,40 L60,60 L70,40 L80,40 L70,70 L60,70 L60,50 L50,70 L40,70 L40,50 Z" />
</vector>
''',

"app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml": '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@android:color/black" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
''',

"app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml": '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@android:color/black" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
''',

"app/src/main/res/xml/backup_rules.xml": '''<?xml version="1.0" encoding="utf-8"?>
<full-backup-content />
''',

"app/src/main/res/xml/data_extraction_rules.xml": '''<?xml version="1.0" encoding="utf-8"?>
<data-extraction-rules>
    <cloud-backup />
    <device-transfer />
</data-extraction-rules>
''',

"app/proguard-rules.pro": '''# default
''',

# ---- FIXED workflow: без gradle-wrapper.jar ----
".github/workflows/build-apk.yml": '''name: Build Unanx APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: 'zulu'
          java-version: '17'

      - name: Install Gradle
        run: |
          wget -q https://services.gradle.org/distributions/gradle-8.7-bin.zip -O /tmp/gradle.zip
          sudo unzip -q /tmp/gradle.zip -d /opt
          sudo ln -sf /opt/gradle-8.7/bin/gradle /usr/local/bin/gradle
          gradle --version

      - name: Build Debug APK
        run: gradle assembleDebug --no-daemon --stacktrace

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: unanx-debug-apk
          path: app/build/outputs/apk/debug/app-debug.apk
          retention-days: 30
''',
}

def main():
    for path, content in FILES.items():
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        print(f"  ✓ {path}")
    print(f"\n✅ Готово: {len(FILES)} файлов создано.")

if __name__ == "__main__":
    main()