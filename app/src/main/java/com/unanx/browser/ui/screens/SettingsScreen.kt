package com.unanx.browser.ui.screens

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
