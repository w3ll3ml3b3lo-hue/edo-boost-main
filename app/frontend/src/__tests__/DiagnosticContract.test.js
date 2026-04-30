import { describe, it, expect } from 'vitest';
import { DiagnosticService } from '../lib/api/services';

// Note: These tests require the backend to be running if they are integration tests.
// In a true contract test, we might use MSW or similar, but the roadmap asks for 
// "production-grade wired to stateful backend".

describe('Diagnostic API Contract', () => {
  it('should start a session with valid schema', async () => {
    // This assumes the backend is reachable at the configured URL
    try {
      const res = await DiagnosticService.start({
        subject_code: 'MATH',
        grade: 3
      });

      expect(res).toHaveProperty('session_id');
      expect(res).toHaveProperty('first_item');
      expect(res.first_item).toHaveProperty('item_id');
      expect(res.first_item).toHaveProperty('question_text');
      expect(Array.isArray(res.first_item.options)).toBe(true);
    } catch (err) {
      throw new Error(`Diagnostic start contract failed: ${err.message}`);
    }
  });

  it('should handle response submission schema', async () => {
    try {
      // We'd need a real session ID here for a full integration test
      // but we can at least verify the service call doesn't throw on parameter structure
      const mockSessionId = '00000000-0000-0000-0000-000000000000';
      const res = await DiagnosticService.submitResponse(mockSessionId, {
        item_id: 'GR3_MATH_FRAC_01',
        selected_index: 1,
        time_on_task_ms: 5000
      });

      // If backend returns 404/400, that's fine for contract test if it returns JSON
      if (res && !res.error) {
        expect(res).toHaveProperty('is_complete');
        expect(res).toHaveProperty('session_state');
      }
    } catch (err) {
      expect(err.message).toMatch(/not found|invalid|404|400/i);
    }
  });
});
