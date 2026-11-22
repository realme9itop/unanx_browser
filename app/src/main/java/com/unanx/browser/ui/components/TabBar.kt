package com.unanx.browser.ui.components

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
