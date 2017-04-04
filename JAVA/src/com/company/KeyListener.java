package com.company;

import org.jnativehook.keyboard.NativeKeyEvent;
import org.jnativehook.keyboard.NativeKeyListener;

public class KeyListener implements NativeKeyListener {
    public void nativeKeyPressed(NativeKeyEvent e) {
        Main.triggerPress(String.valueOf(e.getKeyCode()),
                Long.valueOf(System.currentTimeMillis()).toString());
    }


    public void nativeKeyReleased(NativeKeyEvent e) {
        Main.triggerRelease(String.valueOf(e.getKeyCode()),
                Long.valueOf(System.currentTimeMillis()).toString());
    }

    public void nativeKeyTyped(NativeKeyEvent e) {
        //
    }
}