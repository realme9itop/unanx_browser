package com.unanx.browser.ui.theme

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
