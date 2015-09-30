package edu.umich.clarity;


import sun.jvmstat.monitor.MonitorException;
import sun.jvmstat.monitor.MonitoredHost;
import sun.jvmstat.monitor.MonitoredVm;
import sun.jvmstat.monitor.VmIdentifier;
import sun.tools.jstat.Arguments;
import sun.tools.jstat.OptionFormat;
import sun.tools.jstat.OptionOutputFormatter;
import sun.tools.jstat.OutputFormatter;

/**
 * Extract functions of jstat utility and allow to be integrated into customized profiling.
 *
 * @author hailong
 */
public class JVMProfiler {
    private static final String option = "-gcutil";
    private static String[] profile_arugments = new String[2];
    private static Arguments arguments;
    private static MonitoredHost monitoredHost;
    private static MonitoredVm monitoredVm;

    public static void main(String[] args) {
        JVMProfiler jvmProfiler = new JVMProfiler("8227");
        int count = 1;
        while (count > 0) {
            jvmProfiler.gcProfile();
            count--;
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        jvmProfiler.detachJVM();
    }

    public JVMProfiler(String vmid) {
        profile_arugments[0] = option;
        profile_arugments[1] = vmid;
        arguments = new Arguments(profile_arugments);
    }

    public String gcProfile() {
        String gcStatistics = "";
        try {
            VmIdentifier vmId = arguments.vmId();
            int interval = arguments.sampleInterval();
            monitoredHost = MonitoredHost.getMonitoredHost(vmId);
            monitoredVm = monitoredHost.getMonitoredVm(vmId, interval);
            OptionFormat format = arguments.optionFormat();
            OutputFormatter formatter = new OptionOutputFormatter(monitoredVm, format);
//            System.out.println(formatter.getHeader());
//            System.out.println(formatter.getHeader().trim().replaceAll(" +", " ").split(" ")[5]);
//            System.out.println(formatter.getHeader().trim().replaceAll(" +", " ").split(" ")[6]);
//            System.out.println(formatter.getHeader().trim().replaceAll(" +", " ").split(" ")[7]);
//            System.out.println(formatter.getHeader().trim().replaceAll(" +", " ").split(" ")[8]);
//            System.out.println(formatter.getRow());
//            System.out.println(formatter.getRow().trim().replaceAll(" +", " ").split(" ")[5]);
//            System.out.println(formatter.getRow().trim().replaceAll(" +", " ").split(" ")[6]);
//            System.out.println(formatter.getRow().trim().replaceAll(" +", " ").split(" ")[7]);
//            System.out.println(formatter.getRow().trim().replaceAll(" +", " ").split(" ")[8]);
            String YGC = formatter.getRow().trim().replaceAll(" +", " ").split(" ")[5];
            String YGCT = formatter.getRow().trim().replaceAll(" +", " ").split(" ")[6];
            String FGC = formatter.getRow().trim().replaceAll(" +", " ").split(" ")[7];
            String FGCT = formatter.getRow().trim().replaceAll(" +", " ").split(" ")[8];
            gcStatistics = YGC + "_" + YGCT + "_" + FGC + "_" + FGCT;
        } catch (MonitorException ex) {

        }
        return gcStatistics;
    }

    public void detachJVM() {
        try {
            monitoredHost.detach(monitoredVm);
        } catch (MonitorException ex) {

        }
    }
}
