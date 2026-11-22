package com.unanx.browser.ui.screens

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
