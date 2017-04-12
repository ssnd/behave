package com.company;



import com.rethinkdb.RethinkDB;
import com.rethinkdb.gen.exc.ReqlError;
import com.rethinkdb.gen.exc.ReqlQueryLogicError;
import com.rethinkdb.model.MapObject;
import com.rethinkdb.net.Connection;




import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;



import java.awt.datatransfer.*;
import java.io.IOException;
import java.util.*;


import java.util.logging.Level;
import java.util.logging.Logger;





public class Main {
    static Map<String, String> releaseQueue = new LinkedHashMap<>();

    static ArrayList keyboardData = new ArrayList();
    static ArrayList mouseData = new ArrayList();
    static ArrayList mouseMoveData = new ArrayList();


    public static int ID;


    public static final int SECOND = 1000;

    public static Timer keyboardTimer;
    public static Timer mouseMoveTimer;

    public static String user_id;


    public static  final RethinkDB r = RethinkDB.r;

    private static Connection conn = r.connection().hostname("localhost").connect();


    public static void main(String[] args) throws InterruptedException, UnsupportedFlavorException, IOException {
        keyboardTimer = new Timer();
        mouseMoveTimer = new Timer();


        Logger logger = Logger.getLogger(GlobalScreen.class.getPackage().getName());
        logger.setLevel(Level.OFF);

        System.out.println("Initialized");



        HashMap<String, ArrayList> new_user = r.table("users").insert(r.hashMap()).run(conn);

        user_id = new_user.get("generated_keys").get(0).toString();



        try {
            GlobalScreen.registerNativeHook();
        }
        catch (NativeHookException ex) {
            System.err.println("There was a problem registering the native hook.");
            System.err.println(ex.getMessage());

            System.exit(1);
        }

        GlobalScreen.addNativeKeyListener(new KeyListener());

        MouseListener mouseListenerObject = new MouseListener();

        GlobalScreen.addNativeMouseListener(mouseListenerObject);
        GlobalScreen.addNativeMouseMotionListener(mouseListenerObject);

    }

     public static void submitKeyboardData(ArrayList data) {
        HashMap<String, ArrayList> new_group = r.table("keypressGroups")
                                                .insert(r.hashMap())
                                                .run(conn);


        String new_group_id = new_group.get("generated_keys").get(0).toString();


        for (int i=0; i<data.size(); i++) {
            Map<String, String> map = (Map<String, String>) data.get(i);

            map.put("keypressGroup_id", new_group_id);
            map.put("user_id", user_id);

            data.set(i, map);
        }


        r.table("keypresses").insert(data).run(conn);

     }


     public static void submitMouseMoveData(ArrayList data) {
          HashMap<String, ArrayList>  new_group = r.table("mouseMoveGroups")
                                                 .insert(r.hashMap())
                                                 .run(conn);

          String new_group_id = new_group.get("generated_keys").get(0).toString();

          for (int i = 0; i < data.size(); i++) {
              Map<String, String> map = (Map<String, String>) data.get(i);

              map.put("mouseMoveGroup_id", new_group_id);
              map.put("user_id", user_id);

              data.set(i, map);

          }

          r.table("mouseMoves").insert(data).run(conn);

     }

     public static void submitMouseData(ArrayList data) {

        for (int i = 0; i < data.size(); i++) {
            Map<String, String> map = (Map<String, String>) data.get(i);

            map.put("user_id", user_id);

            data.set(i, map);

        }

        r.table("mouseEvents").insert(data).run(conn);

    }


    public static void rescheduleMouseMoveTimer() {
        mouseMoveTimer.cancel();
        mouseMoveTimer = new Timer();
        mouseMoveTimer.schedule(new TimerTask() {
            public void run() {

                    System.out.println("sending mouse move data to the server");
                    submitMouseMoveData(mouseMoveData);


            }
        }, 1*SECOND);
    }


    public static void rescheduleKeyboardTimer() {
        keyboardTimer.cancel();
        keyboardTimer = new Timer();
        keyboardTimer.schedule(new TimerTask() {
            public void run() {
                System.out.println("sending typing data to the server");
                submitKeyboardData(keyboardData);
            }
        }, 2*SECOND);

    }



    public static void triggerPress(String keyCode, String timestamp){
        releaseQueue.put(keyCode, timestamp);
    }




    public static void triggerRelease(String keyCode, String timestamp) throws InterruptedException {
        LinkedHashMap<String, String> keyEventData = new LinkedHashMap<>();

        keyEventData.put("keyPress", releaseQueue.get(keyCode));
        keyEventData.put("keyRelease", timestamp);
        keyEventData.put("keyCode", keyCode);

        keyboardData.add(keyEventData);



        // here the dict reset happens (inside the rescheduleTimer method
        rescheduleKeyboardTimer();



    }

    static String mouseReleaseQueue = "";


    public static void triggerMousePress(String timestamp){
        mouseReleaseQueue = timestamp;
    }

    public static void triggerMouseMove(String x, String y, String timestamp) {
        LinkedHashMap<String, String> mouseMoveEventData = new LinkedHashMap<>();

        mouseMoveEventData.put("x", Integer.valueOf(x).toString() );
        mouseMoveEventData.put("y", Integer.valueOf(y).toString() );
        mouseMoveEventData.put("timestamp", timestamp);

        mouseMoveData.add(mouseMoveEventData);

        rescheduleMouseMoveTimer();


    }

    public static void triggerMouseRelease(String button, String timestamp){
        LinkedHashMap<String, String> mouseEventData = new LinkedHashMap<>();
        mouseEventData.put("mousePress", mouseReleaseQueue);
        mouseEventData.put("mouseRelease", timestamp);
        mouseEventData.put("buttonCode", button);
        mouseData.add(mouseEventData);


        if (mouseData.size() >= 4) {
            submitMouseData(mouseData);

            mouseData.clear();
        }



    }
}
