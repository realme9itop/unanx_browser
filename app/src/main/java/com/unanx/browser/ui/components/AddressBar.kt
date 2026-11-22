package com.unanx.browser.ui.components

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
