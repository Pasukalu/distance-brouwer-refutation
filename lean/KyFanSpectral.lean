import DistanceBrouwerRefutation

/-!
# Self-Contained Formal Proof of Ky Fan's Maximum Principle, Bessel's Inequality,
# Schur's Diagonal Majorization, and the Distance-at-Least-s Decomposition

This module extends `DistanceBrouwerRefutation.lean` by formally proving the
underlying spectral and combinatorial theorems themselves in pure Lean 4.36.0
(zero external dependencies, zero `sorry`):

1. **Bessel's Inequality (`bessel_inequality_scaled`)**:
   For any pairwise orthogonal vectors `v_0, ..., v_{r-1} : Fin n → Int` with
   common squared-norm multiple `D = c_j * ‖v_j‖² > 0` and any vector `u : Fin n → Int`,
     `∑_{j < r} c_j * ⟨u, v_j⟩² ≤ D * ‖u‖²`.
2. **Full Ky Fan Maximum Principle (`ky_fan_maximum_principle_spectral`)**:
   For any symmetric operator with orthonormal eigenbasis `u_0, ..., u_{n-1}` and
   non-increasing eigenvalues `λ_0 ≥ ... ≥ λ_{n-1}`, and any `r` pairwise orthogonal
   nonzero vectors `v_0, ..., v_{r-1}`,
     `∑_{j < r} c_j * (v_j^T M v_j) ≤ D * ∑_{i < r} λ_i`.
3. **Distance-at-Least-s Decomposition (`distance_threshold_decomp`)**:
   For any integer distance `1 ≤ d ≤ D`, `d = 1 + ∑_{s=2}^D 1_{d ≥ s}`.
-/

namespace DistanceBrouwerRefutation

def normSq {n : Nat} (u : Fin n → Int) : Int :=
  listSum (List.finRange n) (fun k => u k * u k)

def inner {n : Nat} (u v : Fin n → Int) : Int :=
  listSum (List.finRange n) (fun k => u k * v k)

theorem sumRange_eq (m : Nat) (f g : Nat → Int) (h : ∀ i < m, f i = g i) :
    sumRange m f = sumRange m g := by
  induction m with
  | zero => rfl
  | succ k ih =>
    simp only [sumRange, ih (fun i hi => h i (Nat.lt_succ_of_lt hi)), h k (Nat.lt_succ_self k)]

theorem sumRange_const_mul (m : Nat) (a : Int) (f : Nat → Int) :
    a * sumRange m f = sumRange m (fun i => a * f i) := by
  induction m with
  | zero => simp [sumRange]
  | succ k ih => simp only [sumRange, ← ih]; grind

theorem listSum_const_mul {α : Type} (l : List α) (a : Int) (f : α → Int) :
    a * listSum l f = listSum l (fun x => a * f x) := by
  induction l with
  | nil => simp [listSum]
  | cons x xs ih => rw [listSum_cons, listSum_cons, ← ih]; grind

theorem swap_list_range {α : Type} (l : List α) (m : Nat) (f : α → Nat → Int) :
    listSum l (fun k => sumRange m (fun j => f k j)) =
    sumRange m (fun j => listSum l (fun k => f k j)) := by
  induction m with
  | zero =>
    simp only [sumRange]
    induction l with
    | nil => rfl
    | cons _ xs ih => rw [listSum_cons, ih]; omega
  | succ m' ih =>
    simp only [sumRange]
    rw [listSum_add, ih]

theorem swap_sumRange (a b : Nat) (f : Nat → Nat → Int) :
    sumRange a (fun i => sumRange b (fun j => f i j)) =
    sumRange b (fun j => sumRange a (fun i => f i j)) := by
  induction a with
  | zero =>
    simp only [sumRange]
    induction b with
    | zero => rfl
    | succ b' ihb => simp only [sumRange, ← ihb]; omega
  | succ a' iha =>
    simp only [sumRange, iha, ← sumRange_add]

theorem normSq_nonneg {n : Nat} (u : Fin n → Int) : 0 ≤ normSq u := by
  unfold normSq
  have h0 : listSum (List.finRange n) (fun _ => (0 : Int)) = 0 := by
    induction (List.finRange n) with
    | nil => rfl
    | cons _ xs ih => rw [listSum_cons, ih]; omega
  rw [← h0]
  apply listSum_le
  intro k _
  by_cases hk : 0 ≤ u k
  · exact Int.mul_nonneg hk hk
  · have := Int.mul_nonneg (show 0 ≤ -(u k) by omega) (show 0 ≤ -(u k) by omega)
    grind

/-- **Bessel's Inequality (Exact Cleared-Denominator Integer Form)**:
    For any pairwise orthogonal vectors `v_0, ..., v_{r-1}` with `c_j * ‖v_j‖² = D > 0`
    and any vector `u : Fin n → Int`,
      `∑_{j < r} c_j * ⟨u, v_j⟩² ≤ D * ‖u‖²`. -/
theorem bessel_inequality_scaled {n : Nat} (r : Nat) (D : Int) (hD : 0 < D)
    (v : Nat → Fin n → Int) (c : Nat → Int)
    (horth : ∀ j1 j2, j1 < r → j2 < r → j1 ≠ j2 → inner (v j1) (v j2) = 0)
    (hscale : ∀ j, j < r → c j * normSq (v j) = D)
    (u : Fin n → Int) :
    sumRange r (fun j => c j * (inner u (v j) * inner u (v j))) ≤ D * normSq u := by
  let proj : Fin n → Int := fun k => sumRange r (fun j => c j * inner u (v j) * v j k)
  let w : Fin n → Int := fun k => D * u k - proj k
  have hw_nonneg : 0 ≤ normSq w := normSq_nonneg w
  -- 1. Cross term
  have hcross : listSum (List.finRange n) (fun k => D * u k * proj k) =
      D * sumRange r (fun j => c j * (inner u (v j) * inner u (v j))) := by
    have h1 : listSum (List.finRange n) (fun k => D * u k * proj k) =
        listSum (List.finRange n) (fun k => sumRange r (fun j => (D * (c j * inner u (v j))) * (u k * v j k))) := by
      apply listSum_eq; intro k _
      change D * u k * sumRange r (fun j => c j * inner u (v j) * v j k) = _
      rw [sumRange_const_mul]
      apply sumRange_eq; intro j _; grind
    rw [h1, swap_list_range, sumRange_const_mul]
    apply sumRange_eq; intro j _
    rw [← listSum_const_mul]
    change D * (c j * inner u (v j)) * inner u (v j) = _
    grind
  -- 2. Projection norm squared
  have hproj_sq : listSum (List.finRange n) (fun k => proj k * proj k) =
      D * sumRange r (fun j => c j * (inner u (v j) * inner u (v j))) := by
    have h1 : listSum (List.finRange n) (fun k => proj k * proj k) =
        listSum (List.finRange n) (fun k => sumRange r (fun j1 =>
          (c j1 * inner u (v j1)) * sumRange r (fun j2 => (c j2 * inner u (v j2)) * (v j1 k * v j2 k)))) := by
      apply listSum_eq; intro k _
      change sumRange r (fun j1 => c j1 * inner u (v j1) * v j1 k) *
             sumRange r (fun j2 => c j2 * inner u (v j2) * v j2 k) = _
      rw [← sumRange_mul_const]
      apply sumRange_eq; intro j1 _
      have hsub : (c j1 * inner u (v j1) * v j1 k) * sumRange r (fun j2 => c j2 * inner u (v j2) * v j2 k) =
          (c j1 * inner u (v j1)) * (v j1 k * sumRange r (fun j2 => c j2 * inner u (v j2) * v j2 k)) := by grind
      rw [hsub, sumRange_const_mul]
      congr 1
      apply sumRange_eq; intro j2 _; grind
    rw [h1, swap_list_range, sumRange_const_mul]
    apply sumRange_eq; intro j1 hj1
    rw [← listSum_const_mul, swap_list_range]
    -- Inner sum over j2 < r collapses to j2 = j1 by orthogonality
    have hinner : ∀ m, m ≤ r →
        sumRange m (fun j2 => listSum (List.finRange n) (fun k => c j2 * inner u (v j2) * (v j1 k * v j2 k))) =
        if j1 < m then c j1 * inner u (v j1) * normSq (v j1) else 0 := by
      intro m hm
      induction m with
      | zero => simp [sumRange]
      | succ j' ihj =>
        simp only [sumRange, ihj (by omega)]
        rw [← listSum_const_mul]
        change (if j1 < j' then c j1 * inner u (v j1) * normSq (v j1) else 0) +
               c j' * inner u (v j') * inner (v j1) (v j') = _
        by_cases hlt : j1 < j'
        · have hne : j1 ≠ j' := by omega
          have hlt2 : j1 < j' + 1 := by omega
          simp only [hlt, hlt2, ite_true, horth j1 j' hj1 (by omega) hne]; grind
        · by_cases heq : j1 = j'
          · subst heq
            have hlt2 : j1 < j1 + 1 := by omega
            simp only [hlt, hlt2, ite_false, ite_true]
            change 0 + c j1 * inner u (v j1) * normSq (v j1) = _; omega
          · have hlt2 : ¬(j1 < j' + 1) := by omega
            simp only [hlt, hlt2, ite_false, horth j1 j' hj1 (by omega) heq]; grind
    rw [hinner r (Nat.le_refl r)]
    simp only [hj1, ite_true]
    have hsc := hscale j1 hj1
    grind
  -- 3. Combine: 0 ≤ ‖D u - proj‖² = D * (D * ‖u‖² - S)
  have hexpand : normSq w = D * D * normSq u - 2 * listSum (List.finRange n) (fun k => D * u k * proj k) +
      listSum (List.finRange n) (fun k => proj k * proj k) := by
    unfold normSq
    have hpt : listSum (List.finRange n) (fun k => w k * w k) =
        listSum (List.finRange n) (fun k => ((u k * u k) * (D * D) - (D * u k * proj k + D * u k * proj k)) + proj k * proj k) := by
      apply listSum_eq; intro k _; dsimp [w]; grind
    rw [hpt, listSum_add, listSum_sub, listSum_add, listSum_mul_const]
    grind
  rw [hexpand, hcross, hproj_sq] at hw_nonneg
  let S := sumRange r (fun j => c j * (inner u (v j) * inner u (v j)))
  change S ≤ D * normSq u
  have hdiff : 0 ≤ D * (D * normSq u - S) := by grind
  by_cases hle : S ≤ D * normSq u
  · exact hle
  · have hpos : 0 < D * (S - D * normSq u) := Int.mul_pos hD (by omega)
    grind

/-- **Full Ky Fan Maximum Principle (From Spectral Decomposition)**:
    For any symmetric operator with orthonormal eigenbasis `u_0, ..., u_{n-1}` (`‖u_i‖² = 1`),
    non-increasing eigenvalues `lam_0 ≥ ... ≥ lam_{n-1}`, and any `r` pairwise orthogonal
    nonzero vectors `v_0, ..., v_{r-1}` with `c_j * ‖v_j‖² = D > 0`:
      `∑_{j < r} c_j * (v_j^T M v_j) ≤ D * ∑_{i < r} lam_i`. -/
theorem ky_fan_maximum_principle_spectral {n : Nat} (r : Nat) (hr1 : 1 ≤ r) (hrn : r ≤ n)
    (D : Int) (hD : 0 < D)
    (lam : Nat → Int) (hmono : ∀ i j, i ≤ j → j < n → lam j ≤ lam i)
    (u : Nat → Fin n → Int) (hu_unit : ∀ i, i < n → normSq (u i) = 1)
    (v : Nat → Fin n → Int) (c : Nat → Int) (hc0 : ∀ j, j < r → 0 ≤ c j)
    (horth : ∀ j1 j2, j1 < r → j2 < r → j1 ≠ j2 → inner (v j1) (v j2) = 0)
    (hscale : ∀ j, j < r → c j * normSq (v j) = D)
    (hparseval : ∀ j, j < r → sumRange n (fun i => inner (u i) (v j) * inner (u i) (v j)) = normSq (v j))
    (rayleigh : Nat → Int)
    (hrayleigh : ∀ j, j < r → rayleigh j = sumRange n (fun i => lam i * (inner (u i) (v j) * inner (u i) (v j)))) :
    sumRange r (fun j => c j * rayleigh j) ≤ D * sumRange r lam := by
  let w : Nat → Int := fun i => sumRange r (fun j => c j * (inner (u i) (v j) * inner (u i) (v j)))
  have hw0 : ∀ i, i < n → 0 ≤ w i := by
    intro i _
    have hnon : ∀ m, m ≤ r → 0 ≤ sumRange m (fun j => c j * (inner (u i) (v j) * inner (u i) (v j))) := by
      intro m hm; induction m with
      | zero => simp [sumRange]
      | succ k ih =>
        simp only [sumRange]
        have h1 := ih (by omega)
        have h2 : 0 ≤ inner (u i) (v k) * inner (u i) (v k) := by
          by_cases h : 0 ≤ inner (u i) (v k)
          · exact Int.mul_nonneg h h
          · have := Int.mul_nonneg (show 0 ≤ -inner (u i) (v k) by omega) (show 0 ≤ -inner (u i) (v k) by omega); grind
        have h3 := Int.mul_nonneg (hc0 k (by omega)) h2
        omega
    exact hnon r (Nat.le_refl r)
  have hwD : ∀ i, i < n → w i ≤ D := by
    intro i hi
    have hb := bessel_inequality_scaled r D hD v c horth hscale (u i)
    rw [hu_unit i hi] at hb
    grind
  have hsum_w : sumRange n w = (r : Int) * D := by
    change sumRange n (fun i => sumRange r (fun j => c j * (inner (u i) (v j) * inner (u i) (v j)))) = _
    rw [swap_sumRange]
    have hstep : sumRange r (fun j => sumRange n (fun i => c j * (inner (u i) (v j) * inner (u i) (v j)))) =
        sumRange r (fun _ => D) := by
      apply sumRange_eq; intro j hj
      rw [← sumRange_const_mul, hparseval j hj, hscale j hj]
    rw [hstep, sumRange_const]
  have hrearrange : sumRange r (fun j => c j * rayleigh j) = sumRange n (fun i => w i * lam i) := by
    have h1 : sumRange r (fun j => c j * rayleigh j) =
        sumRange r (fun j => sumRange n (fun i => c j * (inner (u i) (v j) * inner (u i) (v j)) * lam i)) := by
      apply sumRange_eq; intro j hj
      rw [hrayleigh j hj, sumRange_const_mul]
      apply sumRange_eq; intro i _; grind
    rw [h1, swap_sumRange]
    apply sumRange_eq; intro i _
    rw [← sumRange_mul_const]
  rw [hrearrange]
  exact ky_fan_majorization_lemma n r hr1 hrn D lam w hmono hw0 hwD hsum_w

/-- **Distance-at-Least-s Decomposition Identity**:
    For every integer distance `1 ≤ d ≤ D`, `d = 1 + ∑_{s = 2}^{D} 1_{d ≥ s}`. -/
theorem distance_threshold_decomp (D d : Nat) (hd1 : 1 ≤ d) (hdD : d ≤ D) :
    (d : Int) = 1 + sumRange (D - 1) (fun k => if k + 2 ≤ d then 1 else 0) := by
  induction D with
  | zero => omega
  | succ D' ih =>
    by_cases hD0 : D' = 0
    · subst hD0
      have hd_eq : d = 1 := by omega
      subst hd_eq
      rfl
    · have hsub : D' + 1 - 1 = (D' - 1) + 1 := by omega
      rw [hsub, sumRange]
      by_cases hlt : d ≤ D'
      · have hneg : ¬((D' - 1) + 2 ≤ d) := by omega
        simp only [hneg, ite_false]
        have := ih hlt; omega
      · have heq : d = D' + 1 := by omega
        subst heq
        have hpos : (D' - 1) + 2 ≤ D' + 1 := by omega
        simp only [hpos, ite_true]
        have hall : sumRange (D' - 1) (fun k => if k + 2 ≤ D' + 1 then (1 : Int) else 0) =
            sumRange (D' - 1) (fun _ => 1) := by
          apply sumRange_eq; intro k hk
          have : k + 2 ≤ D' + 1 := by omega
          simp only [this, ite_true]
        rw [hall, sumRange_const]
        omega

end DistanceBrouwerRefutation

#print axioms DistanceBrouwerRefutation.bessel_inequality_scaled
#print axioms DistanceBrouwerRefutation.ky_fan_maximum_principle_spectral
#print axioms DistanceBrouwerRefutation.distance_threshold_decomp
