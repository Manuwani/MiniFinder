// backend/PatternMatcher.java
import java.util.*;

public class PatternMatcher {
    public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    String algorithm = scanner.nextLine().trim();
    String text = scanner.nextLine();
    String pattern = scanner.nextLine();
    scanner.close();

    long startTime = System.nanoTime();

    List<Integer> result;
    switch (algorithm.toLowerCase()) {
        case "naive":
            result = naiveSearch(text, pattern);
            break;
        case "kmp":
            result = kmpSearch(text, pattern);
            break;
        case "boyer-moore":
            result = boyerMooreSearch(text, pattern);
            break;
        default:
            result = new ArrayList<>();
    }

    long endTime = System.nanoTime();
    long duration = (endTime - startTime) / 1_000_000; // convert to ms

    // Print outputs
    System.out.println("POSITIONS:" + result.toString().replaceAll("[\\[\\]]", ""));
    System.out.println("MATCHES:" + result.size());
    System.out.println("TIME_MS:" + duration);
}


    public static List<Integer> naiveSearch(String text, String pattern) {
        List<Integer> positions = new ArrayList<>();
        int n = text.length(), m = pattern.length();

        for (int i = 0; i <= n - m; i++) {
            int j = 0;
            while (j < m && text.charAt(i + j) == pattern.charAt(j)) j++;
            if (j == m) positions.add(i);
        }
        return positions;
    }

    public static List<Integer> kmpSearch(String text, String pattern) {
        List<Integer> positions = new ArrayList<>();
        int[] lps = computeLPSArray(pattern);
        int i = 0, j = 0;
        while (i < text.length()) {
            if (pattern.charAt(j) == text.charAt(i)) {
                i++; j++;
            }
            if (j == pattern.length()) {
                positions.add(i - j);
                j = lps[j - 1];
            } else if (i < text.length() && pattern.charAt(j) != text.charAt(i)) {
                if (j != 0) j = lps[j - 1];
                else i++;
            }
        }
        return positions;
    }

    public static int[] computeLPSArray(String pat) {
        int[] lps = new int[pat.length()];
        int len = 0, i = 1;
        while (i < pat.length()) {
            if (pat.charAt(i) == pat.charAt(len)) {
                lps[i++] = ++len;
            } else if (len != 0) {
                len = lps[len - 1];
            } else {
                lps[i++] = 0;
            }
        }
        return lps;
    }

    public static List<Integer> boyerMooreSearch(String text, String pattern) {
        List<Integer> positions = new ArrayList<>();
        int[] badChar = new int[256];
        Arrays.fill(badChar, -1);

        for (int i = 0; i < pattern.length(); i++)
            badChar[(int) pattern.charAt(i)] = i;

        int s = 0;
        while (s <= text.length() - pattern.length()) {
            int j = pattern.length() - 1;
            while (j >= 0 && pattern.charAt(j) == text.charAt(s + j)) j--;
            if (j < 0) {
                positions.add(s);
                s += (s + pattern.length() < text.length()) ? pattern.length() - badChar[text.charAt(s + pattern.length())] : 1;
            } else {
                s += Math.max(1, j - badChar[text.charAt(s + j)]);
            }
        }
        return positions;
    }
}
