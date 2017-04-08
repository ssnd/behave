package com.company;

import org.jnativehook.mouse.NativeMouseEvent;
import org.jnativehook.mouse.NativeMouseInputListener;

public class MouseListener implements NativeMouseInputListener {
    public void nativeMouseClicked(NativeMouseEvent e) {
        // action on full click
    }

    public void nativeMousePressed(NativeMouseEvent e) {
        Main.triggerMousePress(Long.valueOf(System.currentTimeMillis()).toString());
    }

    public void nativeMouseReleased(NativeMouseEvent e) {
        Main.triggerMouseRelease(String.valueOf(e.getButton()),Long.valueOf(System.currentTimeMillis()).toString());
    }

    public void nativeMouseMoved(NativeMouseEvent e) {
        Main.triggerMouseMove (Integer.valueOf(e.getX()).toString(), Integer.valueOf(e.getY()).toString(), Long.valueOf(System.currentTimeMillis()).toString());

    }

    public void nativeMouseDragged(NativeMouseEvent e) {
        // action on movement + left click
        // e.getX() // e.getY()
    }
}
