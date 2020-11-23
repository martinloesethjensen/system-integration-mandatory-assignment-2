use serde::{Deserialize, Serialize};

#[allow(non_snake_case)]
#[derive(Serialize, Deserialize)]
pub struct SkatYear {
    Id: i32,
    Label: String,
    CreatedAt: String,
    ModifiedAt: String,
    StartDate: String,
    EndDate: String,
}

#[allow(non_snake_case)]
#[derive(Serialize, Deserialize)]
pub struct SkatUser {
    Id: i32,
    UserId: String,
    CreatedAt: String,
    IsActive: bool,
}

#[allow(non_snake_case)]
#[derive(Serialize, Deserialize)]
pub struct SkatUserYear {
    Id: i32,
    SkatUserId: i32,
    SkatYearId: i32,
    UserId: String,
    IsPaid: bool,
    Amount: i64,
}
